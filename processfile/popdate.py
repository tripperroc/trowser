# Filters twitter json file text field 
# python -OO twep.py TWITTER_FILE REGEX

import sys
import re
import json
import datetime

#Wed, 12 Aug 2009 01:23:04 +0000
#Wed, 12 Aug 2009 01:23:04 +0000

e = datetime.datetime.strptime("Wed, 12 Aug 2012 01:23:04 +0000", "%a, %d %b %Y %X +0000")
def main():
    f = file (sys.argv[1])
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        d = datetime.datetime.strptime(j["created_at"], "%a, %d %b %Y %X +0000")
        total_seconds = (d-e).total_seconds()
        j["time_s"] = int(total_seconds)
        sys.stdout.write("%d %s\n" % (total_seconds, json.dumps(j)))
    f.close()

if __name__ == "__main__":
    main()
