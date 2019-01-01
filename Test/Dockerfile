FROM ubuntu:xenial
RUN apt update; apt upgrade -y;
RUN apt install python3 python-pip wget unzip -y
WORKDIR /root/
ADD https://github.com/shanewiseman/gcp_dns_updater/archive/master.zip ./
RUN unzip master.zip
WORKDIR /root/gcp_dns_updater-master/
RUN pip install -r requirements.txt
COPY google.json.key config/google.json
CMD exec /bin/bash -c "while :; do python main.py; sleep 900; done"
