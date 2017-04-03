import sys
import re
import json
import datetime
import cPickle as pickle

#Wed, 12 Aug 2009 01:23:04 +0000
#Wed, 12 Aug 2009 01:23:04 +0000

def main():
    f = file (sys.argv[1])
    labeled = dict()
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        if j["topic_machine"] == "job" and j["source_machine"] == "personal":
            labeled[j["tweet_id"]] = j
    f.close()
    f = open (sys.argv[2])
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
       
        try:
            if j["id"] in labeled:
                sys.stdout.write("%s" % line)
        except KeyError:
            sys.stderr.write ("%s" % line)
    f.close()
    
if __name__ == "__main__":
    main()
