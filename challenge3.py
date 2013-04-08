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

fileList = []
fileSize = 0
folderCount = 0

try:
    rootdir = sys.argv[1]
    container = sys.argv[2]
except:
    print "script_name local_folder/ container_name"
else: 
    if not os.path.exists(rootdir):
        print "Local folder does not exist! Exiting..."
        sys.exit(1)

    print "Uploading:  %s -> %s" % (rootdir, container)
    cont = cf.create_container(container)

    for root, subFolders, files in os.walk(rootdir):
        folderCount += len(subFolders)
        for file in files:
            f = os.path.join(root,file)
            fileSize = fileSize + os.path.getsize(f)
            print(f)
	    cf.upload_file(cont, f, content_type="text/text")
            fileList.append(f)

    print("Total Size is {0} bytes".format(fileSize))
    print("Total Files ", len(fileList))
    print("Total Folders ", folderCount)
