#!/usr/bin/env python

#Path to Data
outP = "../data/out/"
dataP = "../data/"

#Freifunk map: nodes.json
nodesURL = "http://map.freifunk-bs.de/nodes.json"

import pickle
import urllib
import json
import md5
import os.path
import datetime

def writeRouterStats(ident, name, online, clients):
    "Writes statistics for a router into the corresponding file"
    m = md5.new(ident).hexdigest()
    print m + ", " + ident +", " + ", " + str(online) + ", " + str(clients)

    td = datetime.datetime.now()
    s = td.strftime("%Y%m")
    fn = outP+m+s+".csv"
    f = None
    if not os.path.exists(fn):
        #print "Creating file"
        f = open(fn, "w")
        f.write("#Datetime, online, clients\n")

    if f is  None:
        f = open(fn, "a")
    f.write(td.strftime("%Y/%m/%d %H:%M:%S")+", "+ str(online) + ", " + str(clients) + "\n")
    f.close()

def countClinets(links, i):
    "Counts clients on a node"
    count = 0
    for l in links:
        if (l["source"] == i or l["target"] == i) and l["type"]  == "client":
            count = count + 1
    return count

#Try loading router list
knownRouter = []

try:
    #knownRouter = pickle.load(open(dataP + "router.pickle", "rb"))
    knownRouter = json.loads(open(dataP + "router.json", "r").read())
except:
    print("Failed to load persistent router list")

#Get router list from freifunk map
try:
    nodes = json.loads(urllib.urlopen(nodesURL).read())
    #print("success")
except:
    raise 

#Do some basic format check
if not "nodes" in nodes or not "links" in nodes:
    raise NameError("nodes.json malformed")


links = nodes["links"]
nodes = nodes["nodes"]

router = []
for n in nodes:
    if "flags" in n:
        if "gateway" in n["flags"] and "client" in n["flags"]:
            if  n["flags"]["gateway"] == False and n["flags"]["client"] == False:
                router.append(n)

#look for known routers:
for r in knownRouter:
    node = None
    for n in router:
        if "name" in n:
            if n["id"] == r["id"]:
                node = n

    
    if node == None:
        writeRouterStats(r["id"], r["name"], 0, 0)
    else:
        writeRouterStats(r["id"], r["name"], 1, countClinets(links,nodes.index(node)))
        del router[router.index(node)]
 

#for new routers:
for n in router:
    print "New Router: " + n["id"]

    knownRouter.append({"name": n["name"], "id": n["id"], "md5": md5.new(n["id"]).hexdigest()})

    writeRouterStats(n["id"], n["name"], 1, countClinets(links, nodes.index(n)))


#save router list
try:
#    knownRouter = json.loads(open(dataP + "router.json", "rb").read())
    json.dump(knownRouter, open(dataP + "router.json", "w"))
#    pickle.dump(knownRouter, open(dataP + "router.pickle", "wb"))
except:
    print("Failed to store persistent router list")
    raise

