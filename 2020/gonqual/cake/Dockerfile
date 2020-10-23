FROM ubuntu:20.04

# Setup environ
ENV user cake
ENV prob_port 13200

# Install packages
RUN apt-get update
RUN apt-get install -y socat mailutils
RUN apt-get install -y gdb

# Change permission
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Additional configuration
RUN adduser --disabled-login --gecos "" $user
ADD ./cake /home/$user/cake
ADD ./flag /home/$user/flag

RUN chown -R root:root /home/$user
RUN chown root:$user /home/$user/cake
RUN chown root:$user /home/$user/flag

RUN chmod 755 /home/$user/cake
RUN chmod 440 /home/$user/flag

# final
WORKDIR /home/$user
CMD socat -T 30 TCP-LISTEN:$prob_port,reuseaddr,fork EXEC:/home/$user/cake
USER $user
EXPOSE $prob_port
