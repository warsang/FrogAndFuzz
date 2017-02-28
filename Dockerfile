FROM 	ubuntu:16.04
MAINTAINER warsang <warsang@minet.net> Amre <amre.abouali@telecom-sudparis.eu>


#Defaul command on startup
CMD /bin/bash

#Chane workdir
WORKDIR /home

#Setup packages
RUN echo "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-3.9 main" >> /etc/apt/sources.list.d/clang.list
RUN echo "deb-src http://apt.llvm.org/xenial/ llvm-toolchain-xenial-3.9 main" >>  /etc/apt/sources.list.d/clang.list
RUN apt-get update
RUN apt-get install -y --allow-unauthenticated git make gcc binutils-dev libunwind-dev python2.7 python-pip libffi-dev wget clang-3.9 clang-3.9-doc libclang-common-3.9-dev libclang-3.9-dev libclang1-3.9 libclang1-3.9-dbg libllvm-3.9-ocaml-dev libllvm3.9 libllvm3.9-dbg lldb-3.9 llvm-3.9 llvm-3.9-dev llvm-3.9-doc llvm-3.9-examples llvm-3.9-runtime clang-format-3.9 python-clang-3.9 liblldb-3.9-dev liblldb-3.9-dbg pkg-config zlib1g-dev libglib2.0-dev libpixman-1-dev libfdt-dev 


#Get honggfuzz
RUN git clone https://github.com/google/honggfuzz.git
WORKDIR /home/honggfuzz
RUN make

#Get driller
WORKDIR /home
RUN git clone --recursive https://github.com/PhenixH/driller.git
WORKDIR /home/driller
RUN pip install -r requirements.txt
RUN python2.7 setup.py install

#GET shellphish-qemu (dirty)
WORKDIR /usr/local/lib/python2.7/dist-packages/shellphish_qemu
RUN wget https://raw.githubusercontent.com/PhenixH/shellphish-qemu/master/shellphish_qemu/__init__.py
RUN mv __init__.py.1 __init__.py

#Get qemu and patch
WORKDIR /home
RUN git clone https://github.com/qemu/qemu.git -b stable-2.3
WORKDIR /home/qemu
RUN wget https://raw.githubusercontent.com/shellphish/shellphish-qemu/master/patches/tracer-qemu.patch
RUN git apply tracer-qemu.patch
RUN ./configure --disable-werror
RUN make
WORKDIR /home
RUN mkdir qemu2.3
RUN mv /home/qemu /home/qemu2.3/

#Get tracer
#WORKDIR /home
#RUN git clone --recursive https://github.com/PhenixH/tracer.git -b tracerForFNF
#WORKDIR /home/tracer

#Get fnf
WORKDIR /home
RUN git clone https://github.com/warsang/FrogAndFuzz.git -b develop
WORKDIR /home/FrogAndFuzz
RUN pip install -I --no-use-wheel capstone
RUN pip install config


#GET QEMU2.3 + PATCH
