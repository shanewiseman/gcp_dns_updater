docker build  --build-arg GOOGLE_AUTH=KEY/google.json.key --build-arg ZONE=shanedbwiseman.com. . -t local/google-dns-updater:test
docker run -it local/google-dns-updater:test
