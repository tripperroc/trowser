# Reads a twitter graph file (given as the command line argument), outputs a networkx pkl file.
import networkx as nx
import sys
import re
import json
import os.path as path
import cPickle as pickle

dg = nx.DiGraph ()
gv = set ()
fo = set()
fr = set()
def main():
    deg_fo = long(0)
    deg_fr = long(0)

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
            #s.add(int(j["user_id"]))
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
                else:
                    fo.add(id)
                    deg_fo += 1
                    gv.add(id)
            for id in j["friend_ids"]:
                if id in dg:
                    dg.add_edge(id, int(j["user_id"]))
                    #gg.add_edge(id, j["user_id"])
                else:
                    fr.add(id)
                    deg_fr += 1
                    gv.add(id)
        except ValueError:
            print "ValueError, source line " + str(counter) + ": " + line

    f.close()

    f = open (path.splitext(sys.argv[1])[0] + ".pkl", 'w')
    pickle.dump(dg, f)
    f.close()
    print sys.argv[1]
    print "Users w/ Tweets: %d" % len(dg.nodes())
    print "Friends of Users w/ Tweets: %d" % len(dg.edges())
    print "Fringe Users %d" % len(gv)
    print "Fringe Friends: %d" % (len(fr))
    print "Fringe Followers: %d" % (len(fo))
    print "Ave Friends: %f" % (deg_fr / float(len(dg.nodes())))
    print "Ave Followers: %f" % (deg_fo / float(len(dg.nodes())))
    #g = open (path.splitext(sys.argv[1])[0] + "_full.pkl", 'w')
    #pickle.dump(gg, g)
    #g.close()
if __name__ == "__main__":
    main()
