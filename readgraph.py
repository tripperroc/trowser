# Greps a twitter json file for text content
import networkx as nx
import sys
import re
import json
import os.path as path
import cPickle as pickle

dg = nx.DiGraph ()
gg = nx.DiGraph ()

def main():
    counter = 0
    f = file (sys.argv[1])
    while True:
        line = f.readline()
        if line == "":
            break
        counter += 1
        try:
            j = json.loads(line)
            dg.add_node (int(j["user_id"]))
            # gg.add_node (j["user_id"])
        except ValueError:
            print "ValueError, source line " + str(counter) + ": " + line

    f.close()
    
    f = file (sys.argv[1])
    while True:
        line = f.readline()
        if line == "":
            break
        counter += 1
        try:
            j = json.loads(line)
            for id in j["follower_ids"]:
                if id in dg:
                    dg.add_edge (int(j["user_id"]), id)
                    #gg.add_edge (j["user_id"], id)
            for id in j["friend_ids"]:
                if id in dg:
                    dg.add_edge(id, int(j["user_id"]))
                    #gg.add_edge(id, j["user_id"])
        except ValueError:
            print "ValueError, source line " + str(counter) + ": " + line

    f.close()

    f = open (path.splitext(sys.argv[1])[0] + ".pkl", 'w')
    pickle.dump(dg, f)
    f.close()
if __name__ == "__main__":
    main()
