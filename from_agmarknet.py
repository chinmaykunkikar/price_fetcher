import requests

import config

def fetch_data(url):
    reply = requests.get(url)
    
    if reply.status_code != 200:
        raise Exception("Return code other than 200 - Actual Return Code: %s" % reply.status_code)
    
    return reply.content