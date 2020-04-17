FROM ubuntu:18.04


RUN sed -i s@archive.ubuntu.com@mirrors.aliyun.com@g /etc/apt/sources.list
RUN sed -i s@security.ubuntu.com@mirrors.aliyun.com@g /etc/apt/sources.list
RUN mkdir /root/.pip
RUN echo "[global]\nindex-url =https://mirrors.aliyun.com/pypi/simple/" > /root/.pip/pip.conf 
RUN  apt-get clean

RUN dpkg --add-architecture i386 && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apt-utils git nasm  python python3\
    build-essential \
    python-dev python-pip python-setuptools  python3-pip\
    libc6-dbg \
    libc6-dbg:i386 \
    gcc-multilib \
    gdb-multiarch ltrace strace\
    gcc g++ \
    wget\
    curl \
    glibc-source \
    cmake \
    python-capstone \
    socat \
    netcat \
    ruby ruby-dev\
    xfce4-terminal\
    zsh vim\
    automake autoconf \
    subversion \
    unzip \
    libssl-dev libffi-dev
COPY install.sh install.sh
COPY .zshrc .zshrc
COPY iosevka-fixed-slab-regular.ttf /root/.fonts/iosevka-fixed-slab-regular.ttf
RUN fc-cache -vf
RUN chmod +x ./install.sh
RUN ./install.sh
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN rm install.sh
ENV LANG C.UTF-8
ENV  TERM='xterm-256color'
VOLUME ["/pwn"]
WORKDIR /pwn
CMD [ "/bin/bash" ]
