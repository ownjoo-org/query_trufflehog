# query_trufflehog
test query for trufflehog secrets API

# usage
```
$ python query_trufflehog.py --help
usage: query_trufflehog.py [-h] --domain DOMAIN --client_id CLIENT_ID --client_secret CLIENT_SECRET [--proxies PROXIES]

options:
  -h, --help                      show this help message and exit
  --domain DOMAIN                 The FQDN/IP for your truffelhog host (not full URL)
  --client_id CLIENT_ID           The API key ID to authenticate with
  --client_secret CLIENT_SECRET   The secret for the API key
  --proxies PROXIES               JSON structure specifying 'http' and 'https' proxy URLs
```
