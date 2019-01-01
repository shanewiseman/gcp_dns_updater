import requests
import logging

from GCPDNSUpdater import Updater, RequestRecord, GCPDNSUpdaterException, Config

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main():
    log.warn("=====================================================")
    ip = check_ip()

    log.info("Found IP: {}".format(ip))

    rr = generate_request_record(ip)

    update_record(rr)

    log.warn("=====================================================")

def check_ip():
    return requests.get("https://api.ipify.org").text

def generate_request_record(ip):
    return RequestRecord(ip, Config.HOSTNAME, Config.TTL)

def update_record(rr):
    updater = Updater(Config.ZONE, "config/google.json")

    try:
        updater.update_record(rr)
    except GCPDNSUpdaterException:
        log.warn("Not Updated")


if __name__ == "__main__":
    main()
