FROM ubuntu:20.04
RUN cd /etc/apt && sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' sources.list
RUN cd /etc/apt && sed -i 's/security.ubuntu.com/mirror.kakao.com/g' sources.list
RUN apt-get update -y
RUN apt-get install python3 socat -y
RUN useradd -mU tpu
COPY native.so /home/tpu
COPY tpu.py /home/tpu
COPY flag /flag
CMD /bin/socat tcp-l:1337,reuseaddr,fork EXEC:"/usr/bin/python3 /home/tpu/tpu.py"
