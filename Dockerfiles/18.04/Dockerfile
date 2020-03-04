FROM ubuntu:18.04
RUN  sed -i s@/archive.ubuntu.com/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list
RUN mkdir /root/.pip
RUN echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > /root/.pip/pip.conf 
RUN  apt-get clean

RUN dpkg --add-architecture i386 && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apt-utils git nasm  python \
    build-essential \
    python-dev python-pip python-setuptools \
    libc6-dbg \
    libc6-dbg:i386 \
    gcc-multilib \
    gdb-multiarch ltrace strace\
    gcc g++ \
    wget ca-certificates ssl-cert\
    curl \
    glibc-source \
    cmake \
    python-capstone \
    socat \
    netcat \
    ruby ruby-dev\
    lxterminal \
    zsh vim\
    automake autoconf \
    subversion \
    unzip \
    libssl-dev libffi-dev
COPY install.sh install.sh
COPY .zshrc .zshrc
RUN chmod +x ./install.sh
RUN ./install.sh
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN rm install.sh
ENV LANG C.UTF-8
ENV  TERM='xterm-256color'
VOLUME ["/pwn"]
WORKDIR /pwn
CMD [ "/bin/bash" ]