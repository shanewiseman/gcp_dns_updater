import libcloud
import json
import logging

from libcloud.common.types import LibcloudError
from libcloud.dns.drivers.google import GoogleDNSDriver
from libcloud.dns.types import RecordType
from config import Config


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


