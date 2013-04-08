#!/usr/bin/env python

import os
import sys
import time
import pyrax
import getpass

'''
This entire script is copied and pasted from the examples
The only original part is the sleeps :)
Easy Point
'''

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cdb = pyrax.cloud_databases
instance_name = pyrax.utils.random_name(8)

flavors = cdb.list_flavors()
nm = raw_input("Enter a name for your new instance: ")
print
print "Available Flavors:"
for pos, flavor in enumerate(flavors):
    print "%s: %s, %s" % (pos, flavor.name, flavor.ram)

flav = int(raw_input("Select a Flavor for your new instance: "))
try:
    selected = flavors[flav]
except IndexError:
    print "Invalid selection; exiting."
    sys.exit()

print
sz = int(raw_input("Enter the volume size in GB (1-50): "))

instance = cdb.create(nm, flavor=selected, volume=sz)
print "Name:", instance.name
print "ID:", instance.id
print "Status:", instance.status
print "Flavor:", instance.flavor.name

print "Sleeping for 2 min while instance creates"
time.sleep(120)

instances = cdb.list()
if not instances:
    print "There are no cloud database instances."
    print "Please create one and re-run this script."
    sys.exit()


print
print "Available Instances:"
for pos, inst in enumerate(instances):
    print "%s: %s (%s, RAM=%s, volume=%s) Status=%s" % (pos, inst.name,
            inst.flavor.name, inst.flavor.ram, inst.volume.size, inst.status)
try:
    sel = int(raw_input("Enter the number of the instance to which you want to "
            "add a database: "))
except ValueError:
    print
    print "Invalid (non-numeric) entry."
    print
    sys.exit()
try:
    inst = instances[sel]
except IndexError:
    print
    print "Invalid selection."
    print
    sys.exit()

nm = raw_input("Enter the name of the new database to create in this instance: ")
db = inst.create_database(nm)

dbs = inst.list_databases()
print
print "Database %s has been created." % nm
print "Current databases for instance '%s':" % inst.name
for db in dbs:
    print db.name
print

print "Sleeping for 1 min while %s creates" % nm
time.sleep(60)

instances = cdb.list()
if not instances:
    print "There are no cloud database instances."
    print "Please create one and re-run this script."
    sys.exit()

print
print "Available Instances:"
for pos, inst in enumerate(instances):
    print "%s: %s (%s, RAM=%s, volume=%s) Status=%s" % (pos, inst.name,
            inst.flavor.name, inst.flavor.ram, inst.volume.size, inst.status)
try:
    sel = int(raw_input("Enter the number of the instance to which you want to "
            "add a user: "))
except ValueError:
    print
    print "Invalid (non-numeric) entry."
    print
    sys.exit()
try:
    inst = instances[sel]
except IndexError:
    print
    print "Invalid selection."
    print
    sys.exit()

print
nm = raw_input("Enter the user name: ")
pw = getpass.getpass("Enter the password for this user: ")
print
print "Available Databases:"
dbs = inst.list_databases()
for pos, db in enumerate(dbs):
    print "%s: %s" % (pos, db.name)
print "Enter the numbers of the databases which the user can access,",
print "separated by spaces: ",
selected = raw_input()
selnums = [int(val) for val in selected.split()]
sel_dbs = [db.name for pos, db in enumerate(dbs)
        if pos in selnums]

user = inst.create_user(nm, pw, database_names=sel_dbs)

print
print "User '%s' has been created on instance '%s'." % (nm, inst.name)
print
