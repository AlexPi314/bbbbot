import os
url = os.environ['MONGODB_URL']

import pymongo

client = pymongo.MongoClient(url)
db = client["bbbbot"]