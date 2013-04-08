#!/usr/bin/env python

import os
import sys
import socket
import pyrax
import pyrax.exceptions as exc


creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
dns = pyrax.cloud_dns

'''
This script works with main domain record
It has many holes that will only work with main domain
***For Test Only***
'''

try:
    domain = sys.argv[1]
    ip = sys.argv[2]
except:
    print '''Usage: script.py www.domain.com 127.0.0.1'''
else:
    try:
        dom = dns.find(name=domain)
    except exc.NotFound:
        print '''Domain not found, try another'''
        sys.exit(1)
    else:
        a_rec = {"type": "A",
                "name": domain,
                "data": ip,
                "ttl": 3600}
        recs = dom.add_records([a_rec])
        print recs
