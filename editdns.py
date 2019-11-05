import json
import argparse
import requests
from pprint import pprint
import sys

args = sys.argv

CRN = args[1]
ZONE_ID = args[2]
API_KEY = args[3]
DOMAIN_NAME = args[4]
HOST_NAME = args[5]
ACME_TOKEN = args[6]

print("CRN: %s" % CRN)
print("ZONE_ID: %s" % ZONE_ID)
print("DOMAIN_NAME: %s" % DOMAIN_NAME)
print("HOST_NAME: %s" % HOST_NAME)
print("ACME_TOKEN: %s" % ACME_TOKEN)
print("API_KEY: %s" % API_KEY)

url = "https://iam.cloud.ibm.com/identity/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}
data = "grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey=" + API_KEY

req = requests.post(url, headers = headers, data = data.encode('utf-8'))
resp = json.loads(req.text)

print("body: %s" % resp)
ACCESS_TOKEN = resp['access_token']

print("ACCESS_TOKEN: %s" % ACCESS_TOKEN)
url = 'https://api.cis.cloud.ibm.com/v1/%s/zones/%s/dns_records' % (CRN, ZONE_ID)

print("url: %s" % url)
headers = {
    "Content-Type": "application/json",
    "accept": "application/json",
    "x-auth-user-token": "Bearer " + ACCESS_TOKEN
}

resp = requests.get(url, headers = headers)
zones = json.loads(resp.text)['result']

print("zones:")
pprint(zones)

# Search for existing acme records.
acme_recs = list(filter(lambda e: e['name'].startswith('_acme-challenge') and e['type'] == 'TXT', zones))

print("Existing acme records:")
pprint(acme_recs)

# Remove existing acme records.
for ar in acme_recs:
    print("Deleting %s" % ar['id'])
    url = 'https://api.cis.cloud.ibm.com/v1/%s/zones/%s/dns_records/%s' % (CRN, ZONE_ID, ar['id'])
    requests.delete(url, headers = headers)

# Create new acme record.
url = 'https://api.cis.cloud.ibm.com/v1/%s/zones/%s/dns_records' % (CRN, ZONE_ID)
data = {
    'name': ('_acme-challenge.%s' % DOMAIN_NAME),
    'type': 'TXT',
    'content': ACME_TOKEN
}
print("Creating acme records...")
pprint(data)
requests.post(url, headers = headers, json = data)

print("Done!")
