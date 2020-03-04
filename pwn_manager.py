#!/usr/bin/env python3
from __future__ import print_function
import argparse
import os
import os.path
import docker
import sys
import json
import re
import psutil
import subprocess as sp

from logger import logger
from logging import INFO, DEBUG
from distutils.dir_util import mkpath



EXIST_FLAG = '/tmp/ancypwn.id'
SUPPORTED_UBUNTU_VERSION = [
#    '14.04', Still many issues to be solved (version problems mostly)
    # '16.04',
    '19.04',
    '18.04',
    '19.10',
]

client = docker.from_env()
container = client.containers
image = client.images


class InstallationError(Exception):
    pass

class UnsupportedUbuntuVersion(Exception):
    pass

class AlreadyRuningException(Exception):
    pass

class NotRunningException(Exception):
    pass


def parse_args():
    """Parses commandline arguments
    Returns:
        args -- argparse namespace, contains the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Anciety's pwn environment"
    )
    subparsers = parser.add_subparsers(
        help='Actions you can take'
    )

    run_parser = subparsers.add_parser(
        'run',
        help='run a pwn thread'
    )
    run_parser.add_argument(
        'directory',
        type=str,
        help='The directory which contains your pwn challenge'
    )
    run_parser.add_argument(
        '--ubuntu',
        type=str,
        help='The version of ubuntu to open'
    )
    run_parser.set_defaults(func=run_pwn)

    run_parser.add_argument(
        '--priv',
        action='store_true',
        help='privileged boot, so you can use something like kvm'
    )

    attach_parser = subparsers.add_parser(
        'attach',
        help='attach to running thread',
    )
    attach_parser.set_defaults(func=attach_pwn)

    end_parser = subparsers.add_parser(
        'end',
        help='end a running thread'
    )
    end_parser.set_defaults(func=end_pwn)


    args = parser.parse_args()
    if vars(args) != {}:
        args.func(args)
    else:
        parser.print_usage()


def _get_terminal_size():
    p = sp.Popen('tput cols', shell=True, stdout=sp.PIPE)
    cols = int(p.stdout.read().decode())
    p = sp.Popen('tput lines', shell=True, stdout=sp.PIPE)
    rows = int(p.stdout.read().decode())
    return cols, rows


def _read_container_name():
    if not os.path.exists(EXIST_FLAG):
        raise Exception('Pwn thread is not running')

    container_name = ''
    with open(EXIST_FLAG, 'r') as flag:
        container_name = flag.read()

    if container_name == '':
        os.remove(EXIST_FLAG)
        raise Exception('Meta info corrupted, or unable to read saved info. ' + \
                'Cleaning corrupted meta-info, please shutdown container manually')

    return container_name

def _attach_interactive(name):
    cols, rows = _get_terminal_size()
    if rows and cols:
        cmd = "docker exec -it {} zsh -c \"{}\"".format(
            name,
            'stty cols {} && stty rows {} && zsh'.format(
                cols,
                rows,
            )
        )
    else:
        cmd = "docker exec -it {} '/bin/zsh'".format(
            name,
        )


    os.system(cmd)


def run_pwn(args):
    """Runs a pwn thread
    Just sets needed docker arguments and run it
    """
    if not args.ubuntu:
        ubuntu = '18.04'
    else:
        # check for unsupported ubuntu version
        if args.ubuntu not in SUPPORTED_UBUNTU_VERSION:
            raise UnsupportedUbuntuVersion('version %s not supported!' % args.ubuntu )
        ubuntu = args.ubuntu
    if not args.directory.startswith('~') and \
            not args.directory.startswith('/'):
                # relative path
        args.directory = os.path.abspath(args.directory)

    if not os.path.exists(args.directory):
        raise IOError('No such directory')

    if os.path.exists(EXIST_FLAG):
        raise AlreadyRuningException('Another pwn thread is already running')

    privileged = True if args.priv else False

    # First we need a running thread in the background, to hold existence
    try:
        # check if Xserver is running
        if not "Xquartz" in (p.name() for p in psutil.process_iter()):
            raise Exception("Xserver not started, please open XQuartz first")
            
        display_offset = os.environ['DISPLAY'][os.environ['DISPLAY'].find(':')+1:]
        # find display offset
        os.system("xhost +")
        # open xserver
        running_container = container.run(
            'pwn:{}'.format(ubuntu),
            "/bin/bash -c 'while true;do echo hello docker;sleep 1;done'",
            cap_add=['SYS_ADMIN', 'SYS_PTRACE'],
            detach=True,
            tty=True,
            volumes={
                os.path.expanduser(args.directory) : {
                    'bind': '/pwn',
                    'mode': 'rw'
                },
                os.path.expanduser('~/.Xauthority') : {
                    'bind': '/root/.Xauthority',
                    'mode': 'rw'
                },
                os.path.expanduser('/tmp/.X11-unix') : {
                    'bind': '/tmp/.X11-unix',
                    'mode': 'rw'
                }
            },
            privileged=privileged,
            network_mode='host',
            environment={
                'DISPLAY': "host.docker.internal:"+str(display_offset)
                # 'DISPLAY': os.environ['DISPLAY']
            }
        )
    except Exception as e:
        logger.info("Something wrong happened.")
        raise e

    # Set flag, save the container id
    with open(EXIST_FLAG, 'w') as flag:
        flag.write(running_container.name)


    # Then attach to it, needs to do it in shell since we need
    # shell to do the input and output part(interactive part)
    _attach_interactive(running_container.name)
    

def attach_pwn(args):
    """Attaches to a pwn thread
    Just sets needed docker arguments and run it as well
    """
    container_name = _read_container_name()

    # FIXME Is it better that we just exec it with given name?
    conts = container.list(filters={'name':container_name})
    if len(conts) != 1:
        raise InstallationError('Installation seems to be run. There are more than one image called ancypwn')
    _attach_interactive(conts[0].name)
    

def end_pwn(args):
    """Ends a running thread
    """
    container_name = _read_container_name()
    conts = container.list(filters={'name':container_name})
    if len(conts) < 1:
        os.remove(EXIST_FLAG)
        raise NotRunningException('No pwn thread running, corrupted meta info file, deleted')
    conts[0].stop()
    conts[0].remove()
    os.remove(EXIST_FLAG)
    # os.system('docker rm '+conts[0])



def main():
    parse_args()


if __name__ == "__main__":
    logger.setLevel(INFO)
    main()
