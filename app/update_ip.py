import requests
import json
import os

DDNS_API_KEY=os.getenv('DDNS_API_KEY')
DDNS_DOMAIN='keegoo.freeddns.org'

def get_current_ip():
    return requests.get('https://checkip.amazonaws.com').text.strip()

def get_entry_id(api_key):
    headers = get_auth(api_key)
    url = 'https://api.dynu.com/v2/dns'
    response = requests.get(url, headers=headers)
    domains = response.json()['domains']
    filtered = filter(lambda x: x['name'] == DDNS_DOMAIN, domains)
    entry = next(filtered, None)
    if entry is None:
        return None
    return entry['id']

def get_ddns_ip(api_key, entry_id):
    headers = get_auth(api_key)
    url = f'https://api.dynu.com/v2/dns/{entry_id}'
    response = requests.get(url, headers=headers)
    return response.json()['ipv4Address']

def update_ddns_ip(api_key, entry_id, ipv4):
    headers = get_auth(api_key)
    url = f'https://api.dynu.com/v2/dns/{entry_id}'
    payload = {
        'name': DDNS_DOMAIN,
        'group': '',
        'ipv4Address': ipv4,
        'ipv6Address': None,
        'ttl': 90,
        'ipv4': True,
        'ipv6': True,
        'ipv4WildcardAlias': True,
        'ipv6WildcardAlias': True
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.status_code

def get_auth(api_key):
    return {
        'Content-Type': 'application/json',
        'API-Key': api_key
    }

current_ip = get_current_ip()
id_ = get_entry_id(DDNS_API_KEY)
ddns_ip = get_ddns_ip(DDNS_API_KEY, id_)

if current_ip != ddns_ip:
    print(f'Current IP = {current_ip} and DDNS IP = {ddns_ip} are different.')
    status_code = update_ddns_ip(DDNS_API_KEY, id_, current_ip)
    if (status_code == 200):
        print(f'Update IP = {current_ip} address succeed.')
    else:
        print(f'Update IP = {current_ip} address failed.')
else:
    print(f'No action needed. Current IP and DDNS IP are both {current_ip}.')
