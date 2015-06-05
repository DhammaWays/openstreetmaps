import zipfile
import json

"""
Populate MongoDB database collection "maps"

We directly read zip file (since unncompressed file can be huge).

"""

# Add all the documents to our MongoDB collection "maps"
def add_data(db):
    zf = zipfile.ZipFile('new-delhi_india.osm.zip', 'r')
    f = zf.open('new-delhi_india.osm.json', 'r')
    
    # Go through each line in our JSON file and add it as document to MongoDB
    # collection "maps"
    for line in f:
       db.maps.insert(json.loads(line))
    
    f.close()
    zf.close()

# Return the first document in our maps collection    
def get_data(db):
    return db.maps.find_one()

# Get/Create MongoDB database
def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    
    # 'examples' here is the database name. It will be created if it does not exist.
    db = client.examples
    return db

if __name__ == "__main__":    # For local use
    # Populate our database
    db = get_db() 
    add_data(db)
    print get_data(db) # for sanity check