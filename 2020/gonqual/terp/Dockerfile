# FROM ubuntu:20.04 (hash fixed for future-proofing)
FROM ubuntu@sha256:bc2f7250f69267c9c6b66d7b6a81a54d3878bb85f1ebb5f951c896d13e6ba537

ENV user terpsichore
ENV port 38207

# Install packages
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirror.kakao.com/g" /etc/apt/sources.list
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y socat

# Change tmp permissions
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Add user
RUN adduser --disabled-password --gecos "" $user

# Add files
ADD ./terpsichore /home/$user/terpsichore
ADD ./flag /home/$user/flag

# chown & chmod files
RUN chown -R root:root /home/$user
RUN chown root:$user /home/$user/terpsichore
RUN chown root:$user /home/$user/flag
RUN chmod 2755 /home/$user/terpsichore
RUN chmod 440 /home/$user/flag

# Run server
WORKDIR /home/$user
CMD socat -t 30 -T 30 TCP-LISTEN:$port,reuseaddr,fork EXEC:"/home/$user/terpsichore"
USER $user
EXPOSE $port
