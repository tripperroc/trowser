# Filters twitter json file text field 
# python -OO twep.py TWITTER_FILE REGEX

import sys
import re
import json
import datetime
import cPickle as pickle

#Wed, 12 Aug 2009 01:23:04 +0000
#Wed, 12 Aug 2009 01:23:04 +0000

def main():
    f = file (sys.argv[1])
    d = dict()
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        if "id_str" in j["user"]:
            d[int(j["user"]["id_str"])] = j["user"]["screen_name"]
        else:
            print line
    f.close()
    f = open ("user_dict.pkl", 'w')
    pickle.dump(d, f)
if __name__ == "__main__":
    main()
