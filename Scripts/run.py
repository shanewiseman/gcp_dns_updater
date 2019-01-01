import requests
import logging
import time

from GCPDNSUpdater import Updater, RequestRecord, GCPDNSUpdaterException, Config

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main():

    old_ip = None

    while True:
        found_ip = check_ip()

        log.info("Found IP: {}".format(found_ip))

        if found_ip != old_ip:
            log.warn("=====================================================")

            rr = generate_request_record(found_ip)

            update_record(rr)

            old_ip = found_ip

            log.warn("=====================================================")

        time.sleep(300)

def check_ip():
    return requests.get("https://api.ipify.org").text

def generate_request_record(ip):
    return RequestRecord(ip, Config.HOSTNAME, Config.TTL)

def update_record(rr):
    updater = Updater(Config.ZONE, "GCPDNSUpdater/config/google.json")

    try:
        updater.update_record(rr)
    except GCPDNSUpdaterException:
        log.warn("Not Updated")


if __name__ == "__main__":
    main()
