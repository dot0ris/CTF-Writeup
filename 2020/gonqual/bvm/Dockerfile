FROM ubuntu:20.04

ENV user bvm_xlink
ENV port 63650

# Install packages
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirror.kakao.com/g" /etc/apt/sources.list
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y socat python3 sudo locales

# setup locales
RUN sed -i -e 's/# \(en_US\.UTF-8 .*\)/\1/' /etc/locale.gen
RUN locale-gen && update-locale LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8 \ LANGUAGE=en_US \ LC_ALL=en_US.UTF-8

# Change tmp permissions
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Add user
RUN adduser --disabled-password --gecos "" $user

# Add files
ADD ./ld-2.32.so /home/$user/ld-2.32.so
ADD ./libc-2.32.so /home/$user/libc-2.32.so
ADD ./launcher.py /home/$user/launcher.py
ADD ./buffetvm /home/$user/buffetvm
ADD ./flag /home/$user/flag

# chown & chmod files
RUN chown -R root:root /home/$user
RUN chown root:$user /home/$user/ld-2.32.so
RUN chown root:$user /home/$user/libc-2.32.so
RUN chown root:$user /home/$user/launcher.py
RUN chown root:$user /home/$user/buffetvm
RUN chown root:$user /home/$user/flag
RUN chmod 755 /home/$user/ld-2.32.so
RUN chmod 755 /home/$user/libc-2.32.so
RUN chmod 755 /home/$user/launcher.py
RUN chmod 755 /home/$user/buffetvm
RUN chmod 440 /home/$user/flag

# Run server
WORKDIR /home/$user
CMD socat -t 30 -T 30 TCP-LISTEN:$port,reuseaddr,fork EXEC:"timeout 30 python3 -u /home/$user/launcher.py"
USER $user
EXPOSE $port
