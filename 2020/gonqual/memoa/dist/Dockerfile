FROM ubuntu:18.04

# Setup environ
ENV user memoa
ENV prob_port 13201

# Install packages
RUN apt-get update
RUN apt-get install -y socat

# Change permission
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Additional configuration
RUN adduser --disabled-login --gecos "" $user
ADD ./mms /home/$user/mms
ADD ./flag /home/$user/flag

RUN chown -R root:root /home/$user
RUN chown root:$user /home/$user/mms
RUN chown root:$user /home/$user/flag

RUN chmod 755 /home/$user/mms
RUN chmod 440 /home/$user/flag

# final
WORKDIR /home/$user
CMD socat -T 30 TCP-LISTEN:$prob_port,reuseaddr,fork EXEC:/home/$user/mms
USER $user
EXPOSE $prob_port
