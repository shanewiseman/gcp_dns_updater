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
