import pymongo
# from bson.objectid import ObjectId

db = pymongo.MongoClient().trowser
user_ids = []

for tweet in db.twitter.find():
    user_ids.append(tweet['user']['id_str'])
    # print tweet['user']['id_str']
    # print tweet['geo']
unique_user_ids = set(user_ids)

#loop tweets base on user id
#and store the geo data
for id in unique_user_ids:
    print id
    geo_dict = {}
    for tweet in db.twitter.find({'user.id_str':id}):
        geo_dict.update(tweet['geo'])
        print geo_dict
# print type(unique_user_ids)
print "Done"
