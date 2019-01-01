class GCPDNSUpdaterException(Exception):
    """
    Exception class for handling logic alerts from the main GCPDNSUpdater Class

    Examples of such instance is attempting to update a non existent entry,
    or updating an entry with the same rdata

    """
    pass
