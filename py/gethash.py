#!/usr/bin/env python

#Path to Data
outP = "../data/out/"
dataP = "../data/"

import json
import sys

try:
    knownRouter = json.loads(open(dataP + "router.json", "r").read())
except:
    print("Failed to load persistent router list")
    raise

if len(sys.argv) == 2:
	print "Looking for router: " + sys.argv[1]
	for r in knownRouter:
		if r["name"] == sys.argv[1]:
			print r["md5"]
			sys.exit()
	print "Router nicht gefunden"
else:
	print "Router name as argument needed"

