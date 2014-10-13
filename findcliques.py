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
    global dg
    global ug
    global c
    dg = pickle.load(open(sys.argv[1]))
    # dg <= nx.DiGraph 

    ug = dg.to_undirected(reciprocal=True)

    c = list(nx.find_cliques(ug))

    #c = filter (lambda x: x > 5, c)

    
    
    d, cliques = invert (c)
    #cliques = collections.defaultdict(clique)
    f = file (sys.argv[2])
    while True:
        line = f.readline()
        if line == "":
            break
       # print line
        j = json.loads(line)
        for cliq in d[int(j["user"]["id_str"])]:
            cliq.add(j)
    f.close()

    for c in cliques:
        print json.dumps({"id": c.id, "clique": c.nodes, "size": len(c.nodes), "mean_lat": c.mean_t (), "mean_lon": c.mean_n (), "tweets": c.count, "cov_tt": c.cov_tt(), "cov_nn": c.cov_nn(), "cov_tn": c.cov_tn() })
    
        
    #n, bins, patches = P.hist(map(len, d))
if __name__ == "__main__":
    main()
