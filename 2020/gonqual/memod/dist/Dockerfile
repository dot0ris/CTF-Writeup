FROM ubuntu:18.04

# Setup environ
ENV user memod
ENV prob_port 13202

# Install packages
RUN apt-get update
RUN apt-get install -y sudo socat python3.7 python3-pip
RUN pip3 install pwntools

# Change permission
RUN chmod 1733 /var/tmp /dev/shm
RUN chmod 766 /tmp

# Additional configuration
RUN adduser --disabled-login --gecos "" $user
RUN adduser --disabled-login --gecos "" runner
RUN echo $user' ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
ADD ./mms /home/$user/mms
ADD ./run.py /home/$user/run.py
ADD ./func_test.py /home/$user/func_test.py
ADD ./vuln_test.py /home/$user/vuln_test.py
ADD ./flag_33cb283980501c2a2145bf2a91c86efee96ccfc8dbecfbb92bf284b9010018b0 /home/$user/flag_33cb283980501c2a2145bf2a91c86efee96ccfc8dbecfbb92bf284b9010018b0

RUN chown -R root:root /home/$user
RUN chown root:$user /home/$user/mms
RUN chown root:$user /home/$user/run.py
RUN chown root:$user /home/$user/func_test.py
RUN chown root:$user /home/$user/vuln_test.py
RUN chown root:$user /home/$user/flag_33cb283980501c2a2145bf2a91c86efee96ccfc8dbecfbb92bf284b9010018b0

RUN chmod 440 /home/$user/mms
RUN chmod 755 /home/$user/run.py
RUN chmod 440 /home/$user/func_test.py
RUN chmod 440 /home/$user/vuln_test.py
RUN chmod 440 /home/$user/flag_33cb283980501c2a2145bf2a91c86efee96ccfc8dbecfbb92bf284b9010018b0

# final
WORKDIR /home/$user
CMD socat -T 60 TCP-LISTEN:$prob_port,reuseaddr,fork EXEC:/home/$user/run.py
USER $user
ENV TERM linux
ENV TERMINFO /etc/terminfo
EXPOSE $prob_port
