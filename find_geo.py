import pymongo
from bson.objectid import ObjectId

db = pymongo.MongoClient().trowser

for tweet in db.twitter.find():
    print tweet['user']['id_str']
    print tweet['geo']

print "finish processing"
