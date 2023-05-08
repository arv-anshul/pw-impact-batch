from os import environ

# Dependencies: dnspython pymongo
import pymongo

MONGO_PASS = environ['MONGO_PASS']

# client = pymongo.MongoClient(
#     f"mongodb+srv://arv-mongo-818583:{MONGO_PASS}@cluster0.ol89b59.mongodb.net/?retryWrites=true&w=majority"
# )

db = client['pwskills']

data = {
    'name': 'Anshul Raj',
    'paylod': {
            'database': 'pwskills',
            'client': 'MongoDB'
    }
}

col1 = db['first_collection']

col1.insert_one(data)
