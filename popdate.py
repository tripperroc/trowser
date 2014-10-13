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
        
        sys.stdout.write("%d %s" % ((d-e).total_seconds(), line))
    f.close()

if __name__ == "__main__":
    main()
