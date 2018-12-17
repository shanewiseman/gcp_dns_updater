class Config:
    DNS_USER_ID = "dns-updater@total-display-138423.iam.gserviceaccount.com" # The GCP Service Account ID
    DNS_KEY = "config/google.json" 		# The path to the JSON-key file (relative to the project's root)
    DNS_PROJECT_NAME = "total-display-138423" 	# Your Google Cloud Platform project name

# Example settings for creating an test.mydomain.com A record that points to your current IP
    A_RECORD_TTL_SECONDS = 600 	# The desired TTL for your DNS record
    RECORD_NAME = "shanedbwiseman.com." 		# The record name
    ZONE_FQDN = "shanedbwiseman.com." # The domain zone name (usually the domain with an ending `.`)
