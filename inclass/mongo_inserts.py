# inclass/mongoDB.py

from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

DB_USER = os.getenv("MONGO_USER", default="Invalid DB_USER value")
DB_PW = os.getenv("MONGO_PW", default="Invalid DB_PW value")
ClusterName = os.getenv("MONGO_CLUSTER", default="Invalid ClusterName value")

# connection uri
connection_uri = f"mongodb+srv://{DB_USER}:{DB_PW}@{ClusterName}.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
print("---------------")
print("CONNECTION URI:", connection_uri)

client = pymongo.MongoClient(connection_uri)
print("----------------")
print("CLIENT:", type(client), client)


# "test_database" or whatever you want to call it
db = client.test
print("----------------")
print("DB:", type(db), db)

# "pokemon_test" or whatever you want to call it
collection = db.pokemon_test 
print("----------------")
print("TYPE:", type(collection))
print("COLLECTION:", collection)


# collection.insert_one({
#     "name": "Pikachu",
#     "level": 30,
#     "exp": 76000000000,
#     "hp": 400,
# })

print("DOCS:")
print("--------------------------------------------")
print(collection.count_documents({"name": "Pikachu"}))

print("----------------")
print("COLLECTIONS:")
print(db.list_collection_names({}))

