# Greps a twitter json file for text content
import networkx as nx
import sys
import re
import json
import os.path as path
import cPickle as pickle
import numpy as np
import pylab as P
import collections

def safediv (num, div):
    if div != 0:
        return num/div
    else:
        return 0
    
class clique:

    id = 0;
    def __init__(self, n):
        self.nodes = n
        self.mean_lat = 0.0
        self.mean_latq = 0.0
        self.mean_lon = 0.0
        self.mean_lonq = 0.0
        self.mean_lat_lon = 0.0
        self.count = 0
        self.id = clique.id
        clique.id += 1
        
    #def clique:
    #   mean_lat = mean_latq = mean_lon = mean_lonq = mean_lat_lon = 0.0
    #    count = 0

    def add (self, tweet):
        lat = tweet["geo"]["latitude"]
        lon = tweet["geo"]["longitude"]
        self.count += 1
        self.mean_lat += lat
        self.mean_latq += lat * lat
        self.mean_lon += lon
        self.mean_lonq += lon * lon
        self.mean_lat_lon += lat * lon


    def cov_tt (self):
        return safediv(self.mean_latq, self.count) - self.mean_t() * self.mean_t()

    def cov_nn (self):
        return safediv(self.mean_lonq, self.count) - self.mean_n() * self.mean_n()

    def cov_tn (self):
        return safediv(self.mean_lat_lon, self.count) - self.mean_t() * self.mean_n()

    def mean_n (self):
        return safediv(self.mean_lon, self.count)

    def mean_t (self):
        return safediv(self.mean_lat, self.count)
     
def invert (c):
    d = collections.defaultdict (list)
    e = list()
    
    for cliq in c:
        cl = clique(cliq)
        #print len(cliq)
        for node in cliq:
            d[node].append(cl)
        e.append(cl)
    return d, e
            
def main():
    global ug
    global c

    ug = nx.Graph()
    c = file (sys.argv[1])
  
    
    click_dict = dict()
    node_dict = collections.defaultdict(list)
    while True:
        line = c.readline()
        if line == "":
            break
       # print line
        j = json.loads(line)
        if j["tweets"] > 0:
            click_dict[j["id"]] = j
            for node in j["clique"]:
                node_dict[node].append(j)
    c.close()
    for k,v in node_dict.iteritems():
        for i in range(0,len(v)):
            for j in range(i+1, len(v)):
                ug.add_edge(v[i]["id"], v[j]["id"], {"width": len(set(v[i]["clique"]) & set(v[j]["clique"])), "size": min(v[i]["size"], v[j]["size"]), "v1_lat" : v[i]["mean_lat"], "v1_lon" : v[i]["mean_lon"] , "v2_lat" : v[j]["mean_lat"], "v2_lon" : v[j]["mean_lon"] })

    for v1, v2 in ug.edges_iter():
        d = ug.get_edge_data (v1, v2)
        print json.dumps ({"v1": v1, "v2": v2, "width": d["width"], "size" : d["size"], "v1_lat": d["v1_lat"], "v1_lon": d["v1_lon"], "v2_lat": d["v2_lat"], "v2_lon": d["v2_lon"]})
    
        
    #n, bins, patches = P.hist(map(len, d))
if __name__ == "__main__":
    main()
