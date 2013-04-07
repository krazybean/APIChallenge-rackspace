#!/usr/bin/env python

import os
import sys
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

'''
ins_count - Instance Count: Number of instances to create
ins_name - Instance Name: Server Prefix (example: web_, node_, server_,...)
ins_size - Instance Size: Slice Size : (example: 512, 1024, 2048, 4096,...)
ins_flavor - Instance Flavor : (example: CentOS 6.2, Fedora 17,...)
'''
ins_count = 3
ins_name = 'node_'
ins_size = '512'
ins_flavor = 'CentOS 6.2'

def refID (prefix, value):
    if prefix == 'ins_flavor':
	for img in cs.images.list():
            if value in img.name:
                return img.id
    elif prefix == 'ins_size':
        for size in cs.flavors.list():
            if value in str(size.ram):
                return size.id
    else:
        pass

ins_size_id = refID('ins_size', ins_size)
ins_flavor_id = refID('ins_flavor', ins_flavor)

def clear_file():
    open('.cloud_servers', 'w').close()

def log_manage(action, servername, passwd=None):
    '''Function to log existing slices or newly added and await IP completion'''
    if action == 'add':
        log = open(".cloud_servers", "ab+")
        log.write("ServerName: %s, Password: %s %s" % (servername, passwd, '\n'))
        log.close()
    elif action == 'list':
        log = open(".cloud_servers", "r")
        log_data = log.read()
        for s in log_data.split('\n'):
            if servername in s:
                '''returns stored password'''
                return s.split(',')[1]
    else: pass

'''User Actions'''
try:
    if sys.argv[1] == '--create':
        c = 0
        while c < ins_count:
            serv_name = '''%s%s''' % (ins_name, c)
            server = cs.servers.create(serv_name, ins_flavor_id, ins_size_id)
            log_manage('add', server.name, server.adminPass)
            print "Networks:", server.networks
            print "Admin Password:", server.adminPass
            c = c + 1

    if sys.argv[1] == '--list':
        servers = cs.servers.list()
        for s in servers:
            try:
                serv_net_1, serv_net_2 = s.networks['public'][0],s.networks['public'][1]
            except KeyError:
                serv_net_1, serv_net_2 = '0.0.0.0', '::::'
            try:
               creds = log_manage('list', s.name)
            except:
               creds = ''
            print s.name, serv_net_1, serv_net_2, s.status, creds

    if sys.argv[1] == '--clear':
        clear_file()

except IndexError:
    print '''Usage: --list, --create, --clear'''

