# ------------------ COUCHUTILS ---------------------------#
import time
import couchdb
import os.path
import re
import sys,logging,socket

basepath = os.path.dirname(__file__)

cpath = os.path.abspath(os.path.join(basepath, "..", "conf"))
CREDENTIALHOME = cpath + "/couchcred.conf"

# --------- END Logger configuration -------- #

def getcreds(location):
	f = open(location, "rb")
	for line in f:
		if "username" in line:
			user = re.sub("username ", "", line)
			user=user.rstrip()
		if "password" in line:
			pwd = re.sub("password ", "", line)
			pwd=pwd.rstrip()
	return user, pwd

#Connection info for couchdb
couch = couchdb.Server('http://couch.snopl.us')
couchuser, couchpassword = getcreds(CREDENTIALHOME)
couch.resource.credentials = (couchuser, couchpassword)

#Allows one to connect to a couchdb
def connectToDB(dbName):
    status = "ok"
    db = {}
    numtries = 0
    while numtries < 3:
        try:
           db = couch[dbName]
           break
        except:
            print "Failed to connect to " + dbName
            logging.exception("Failed to connect to " + dbName)
            numtries += 1
            logging.info("At try " + str(numtries) + ". Trying again..")
            time.sleep(1)
            status = "bad"
            continue
    return status, db

#--------------- /COUCHUTILS ------------------------------#
