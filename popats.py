# Filters twitter json file text field 
# python -OO twep.py TWITTER_FILE REGEX

import sys
import re
import json
import datetime

#Wed, 12 Aug 2009 01:23:04 +0000
#Wed, 12 Aug 2009 01:23:04 +0000

e = datetime.datetime.strptime("Wed, 12 Aug 2012 01:23:04 +0000", "%a, %d %b %Y %X +0000")
p = re.compile('@\w+')
def main():
    f = file (sys.argv[1])
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        l = p.findall(j["text"])
        l = set(map((lambda x : x[1:]), l))
        l.add(j["user"]["screen_name"])
        if "to_user" in j:
             l.add(j["to_user"])
        j["players"] = list(l)
        j["num_players"] = len(j["players"])
        sys.stdout.write("%s\n" % json.dumps(j))
    f.close()

if __name__ == "__main__":
    main()
