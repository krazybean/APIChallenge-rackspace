#!/usr/bin/env python

import os
import sys
import time
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

try: 
    sys.argv[1]
except IndexError: 
    print '--clone, --list'
else:
    if sys.argv[1] == '--clone':
        servers = cs.servers.list()
        srv_dict = {}
        print "Select a server from which an image will be created."
        for pos, srv in enumerate(servers):
            print "%s: %s" % (pos, srv.name)
            srv_dict[str(pos)] = srv.id
            selection = None
        while selection not in srv_dict:
            if selection is not None:
                print "   -- Invalid choice"
            selection = raw_input("Enter the number for your choice: ")

        server_id = srv_dict[selection]
        print
        nm = raw_input("Enter a name for the image: ")

        img_id = cs.servers.create_image(server_id, nm)

        print "Cloning Server ID: %s" % img_id
        server_name = "%s_clone" % nm
        '''Change Size ID based on Size'''
        size = 2

        print "Sleeping for 3min, cannot create from busy image..."
        '''Change sleep duration for slice size'''

        time.sleep(180)
 
        server = cs.servers.create(server_name, img_id, size)

        time.sleep(60)
        print "Name:", server.name
        print "ID:", server.id
        print "Status:", server.status
        print "Admin Password:", server.adminPass
        print "Networks:", server.networks

    if sys.argv[1] == '--list':
        imgs = cs.images.list()
        for img in imgs:
            print "Name: %s\n    ID: %s" % (img.name, img.id)

