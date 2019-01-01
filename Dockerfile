FROM ubuntu:xenial

WORKDIR /root/
COPY apt-requirements.txt /root/
RUN apt update; apt upgrade -y;
RUN cat apt-requirements.txt | xargs apt install -y 

COPY pip-requirements.txt /root/
RUN pip3 install -r pip-requirements.txt

COPY GCPDNSUpdater/ /root/google-dns-updater/GCPDNSUpdater/  
ENV PYTHONPATH=/root/google-dns-updater/

WORKDIR /root/google-dns-updater/

ARG GOOGLE_AUTH
COPY ${GOOGLE_AUTH} GCPDNSUpdater/config/google.json

ARG ZONE
ENV ZONE=${ZONE}
CMD exec /bin/bash -c "PYTHONPATH=${PYTHONPATH}:/root/google-dns-updater/;python3 -c 'from GCPDNSUpdater import GCPDNSUpdaterTest; GCPDNSUpdaterTest(\"${ZONE}\", \"GCPDNSUpdater/config/google.json\").run()'"
