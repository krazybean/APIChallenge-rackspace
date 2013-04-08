#!/usr/bin/env python

import os
import sys
import pyrax
import pyrax.exceptions as exc
import pyrax.utils as utils

'''
Warning this script uploads recursively
'''

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles

try:
    container = sys.argv[1]
except:
    print "script_name  container_name"
else:
    cont = cf.create_container(container)
    print "New Container"
    print "Name:", cont.name
    print "# of objects:", cont.object_count
    print
    print "All Containers"
    print "list_containers:", cf.list_containers()
    print "get_all_containers:", cf.get_all_containers()

