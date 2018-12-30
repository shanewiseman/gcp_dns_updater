import libcloud
import json
import logging

from libcloud.common.types import LibcloudError
from libcloud.dns.drivers.google import GoogleDNSDriver
from libcloud.dns.types import RecordType
from config import Config

class GCPDNSUpdaterTest:
    """

    Class containing all unit tests for existing logic. Addition logic in GCPDNSUpdater
    class should be associated with a new test here

    """

log = logging.getLogger(__name__)

class GCPDNSUpdaterTest:

    """

    Class containing all unit tests for existing logic. Addition logic in GCPDNSUpdater
    class should be associated with a new test here

    """

    def __init__(self, zone_fqdn, google_auth_json_file):
        self.fqdn = zone_fqdn
        self.google_auth_json_file = google_auth_json_file

    def run(self):
        for test in [self.test_create_object,
                self.test_format_record_name,
                self.test_create_delete_record,
                self.test_create_existing_record,
                self.test_delete_nonexist_record,
                self.test_update_record,
                self.test_update_same_record,
                self.test_update_nonexist_record]:

            test()

        log.warning("All Tests Passed")


    def test_create_object(self):
        log.warning("test_create_object")
        a = GCPDNSUpdater(self.fqdn, self.google_auth_json_file)

        return True


    def test_format_record_name(self):
        log.warning("test_format_record_name")
        permutations = [("a", "a.{}".format(self.fqdn)),
                ("a.", "a."),
                ("a.b.c", "a.b.c.{}".format(self.fqdn)),
                ("a.b.c.", "a.b.c.")]

        a = GCPDNSUpdater(self.fqdn, self.google_auth_json_file)
        for i in permutations:
            if a.format_record_name(i[0]) != i[1]:
                raise Exception()

        return True


    def test_create_delete_record(self):
        log.warning("test_create_delete_record")
        a = GCPDNSUpdater(self.fqdn, self.google_auth_json_file)
        rr = RequestRecord(ip="1.1.1.1",hostname="test")
        a.create_record(rr)
        a.delete_record(rr)


    def test_create_existing_record(self):
        log.warning("test_create_existing_record")
        a = GCPDNSUpdater(self.fqdn, self.google_auth_json_file)
        rr = RequestRecord(ip="1.1.1.1",hostname="test")
        a.create_record(rr)

        try:
            a.create_record(rr)
        except GCPDNSUpdaterException:
            a.delete_record(rr)
            return True

        raise Exception()


    def test_delete_nonexist_record(self):
        log.warning("test_delete_nonexist_record")
        a = GCPDNSUpdater(self.fqdn, self.google_auth_json_file)
        rr = RequestRecord(ip="1.1.1.1",hostname="test")

        try:
            a.delete_record(rr)
        except GCPDNSUpdaterException:
            return True

        raise Exception()


    def test_update_record(self):
        log.warning("test_update_record")
        a = GCPDNSUpdater(self.fqdn, self.google_auth_json_file)
        rr = RequestRecord(ip="1.1.1.1",hostname="test")
        a.create_record(rr)
        rr = RequestRecord(ip="1.1.1.2",hostname="test", ttl=10)
        a.update_record(rr)
        a.delete_record(rr)
        return True


    def test_update_same_record(self):
        log.warning("test_update_same_record")
        a = GCPDNSUpdater(self.fqdn, self.google_auth_json_file)
        rr = RequestRecord(ip="1.1.1.1",hostname="test")
        a.create_record(rr)
        try:
            a.update_record(rr)
        except GCPDNSUpdaterException:
            a.delete_record(rr)
            return True

        raise Exception()


    def test_update_nonexist_record(self):
        log.warning("test_update_nonexist_record")

        a = GCPDNSUpdater(self.fqdn, self.google_auth_json_file)
        rr = RequestRecord(ip="1.1.1.1",hostname="test")
        try:
            a.update_record(rr)
        except GCPDNSUpdaterException:
            return True

        raise Exception()


####################################################################################################
####################################################################################################


class GCPDNSUpdaterException(Exception):
    """
    Exception class for handling logic alerts from the main GCPDNSUpdater Class

    Examples of such instance is attempting to update a non existent entry,
    or updating an entry with the same rdata

    """
    pass


class RequestRecord:
    """

    Object used by GCPDNSUpdater for all record mutations, contains record information

    Args:
        ip (string) Ip address of hostname record
        hostname (string) dns hostname for record
        ttl (string)(optional) TimeToLive attribue for record

    """

    def __init__(self, ip, hostname, ttl=None):
        self.ip = ip
        self.hostname = hostname
        self.ttl = ttl or "3600"


class GCPDNSUpdater:
    """
    Class for the creation, deletion, and mutation of records in the GCP DNS envirnment

    All mutable calls require an instance of RequestRecord

    (Throws) GCPDNSUpdaterException(Exception)

    """
    """
    TODO:
        1) need to check to see if the class variable (zone) is updated at the same time
            or do we need to re_initize internal zone object.
            Currently, we don't make use of long lived zone objects, but I can see how this
            be benficial to track

    """


    def __init__(self, zone_fqdn, google_auth_json_file):
        """
        Class Constructor

        (Args):
            zone_fqdn (string) root domain name of zone (ie zone.com)
            google_auth_json_file (string path) relative path for google_auth construct

        log.debug("Zone: {} Authfile: {}".format(zone_fqdn, google_auth_json_file))
        self.google_auth = self.parse_auth_file(google_auth_json_file)
        self.dns_driver = self.create_driver(google_auth_json_file)
        self.zone = self.retrieve_zone(zone_fqdn)


    def parse_auth_file(self, auth_file):
        """
        Returns structured object from file containing JSON

        (Args):
            auth_file (string path) relative path for google_auth construct
                (ie config/google_auth.file)(https://cloud.google.com/compute/docs/access/service-accounts)

        """

        with open(auth_file) as f:
            return json.load(f)


    def create_driver(self, auth_file):
        """
        Generates driver class which interacts with GCP Directly

        (Args):
            auth_file (string path) relative path for google_auth construct
                (ie config/google_auth.file)(https://cloud.google.com/compute/docs/access/service-accounts)

        """
        log.info("Creating Driver")
        return GoogleDNSDriver(
                self.google_auth['client_email'],
                auth_file,
                self.google_auth['project_id'])


    def retrieve_zone(self, zone_fqdn):
        """
        Retrives Zone object from driver based upon zone matching passed fqdn

        (Args):
            zone_fqdn (string) root domain name of zone (ie zone.com)

        (throws)
            raises GCPDNSUpdaterException if zone is not matched

        """

        log.info("Retrieving Zone")
        for zone in self.dns_driver.iterate_zones():
            if zone_fqdn == zone.domain:
                log.info("Found Zone")
                log.debug("{}".format(vars(zone)))
                return zone

        raise GCPDNSUpdaterException("Zone Not Found: {}".format(zone_fqdn))

    def create_record(self, rr):
        """
        creates and commits record to zone

        (Args):
            RequestRecord()

        (throws)
            raises GCPDNSUpdaterException if record already exists on GCP

        """
        log.info("Creating Record")
        fqdn = self.format_record_name(rr.hostname)

        try:
            self.retrieve_record(fqdn)
        except GCPDNSUpdaterException:
            return self.dns_driver.create_record(
                    fqdn,
                    self.zone,
                    RecordType.A,
                    {'ttl' : rr.ttl, 'rrdatas' : [rr.ip]})

        raise GCPDNSUpdaterException("Record Already Exists, Can't Create {}".format(fqdn))


    def delete_record(self, rr):
        """
        deletes record existing in GCP

        (Args):
            RequestRecord()

        (throws)
            raises GCPDNSUpdaterException if record does NOT exist on GCP

        """
        log.info("Deleting Record")
        fqdn = self.format_record_name(rr.hostname)
        record = None
        try:
            record = self.retrieve_record(fqdn)
        except GCPDNSUpdaterException:
            raise GCPDNSUpdaterException("Record Does Not Exists, Can't Delete {}".format(fqdn))

        return self.dns_driver.delete_record(record)

    def update_record(self, rr):
        """
        updates record existing in GCP

        (Args):
            RequestRecord()

        (throws)
            raises GCPDNSUpdaterException if record does NOT exist on GCP
            raises GCPDNSUpdaterException if record in GCP is identical to update

        """
        log.info("Updating Record")

        fqdn = self.format_record_name(rr.hostname)
        log.info("Hostname: {}".format(fqdn))

        record = self.retrieve_record(fqdn)

        if self.eligible_for_update(record, rr):

            log.info("Performing Update")
            self.delete_record(rr)
            return self.create_record(rr)
            #str(fqdn[0:fqdn.find(self.zone.domain)]),

        raise GCPDNSUpdaterException("Record Matches Existing, Can't Update")

    def format_record_name(self, hostname):
        """
        Formats record as required for driver usage

        (Args):
            hostname (string) base hostname for record (ie wwww)

        """
        #NOTE in case user provides provides fqdn or we're mutating the base zone hostname
        if hostname[-1] == ".":
            return hostname

        return "{}.{}".format(hostname,self.zone.domain)


    def retrieve_record(self, hostname):
        """
        retrives record existing in GCP (Requires FQDN)

        log.info("Retrieving Record")
        for record in self.dns_driver.iterate_records(self.zone):
            if record.type != RecordType.A:
                continue
            if hostname == record.name:
                log.info("Found Record")
                log.debug("{}".format(vars(record)))
                return record

        log.info("Record Not Found")
        raise GCPDNSUpdaterException("Record Not Found: {}".format(hostname))


    def eligble_for_update(self,record, rr):

        """
        Checks if record matches the Request Record

        (Args):
            GoogleDNSDriver:Record()
            RequestRecord()
        """

	log.info(record)
        if str(record.ttl) == str(rr.ttl) and str(record.data["rrdatas"][0]) == str(rr.ip):
	    log.info("Not Eligible For Update")
            return False
	log.info("Eligible For Update")
        return True
