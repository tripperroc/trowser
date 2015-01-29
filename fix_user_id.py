# Filters twitter json file text field 
# python -OO twep.py TWITTER_FILE REGEX

import sys
import re
import json

def main():
    f = file (sys.argv[1])

    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        if "user" in j:
            if "id" in j["user"]:
                j["screen_name"] = j["user"]["screen_name"]
                sys.stdout.write("%s\n" % json.dumps(j))
    f.close()

if __name__ == "__main__":
    main()
