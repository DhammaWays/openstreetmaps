import zipfile
import json

def add_data(db):
    data = []
    zf = zipfile.ZipFile('new-delhi_india.osm.zip', 'r')
    f = zf.open('new-delhi_india.osm.json', 'r')
    for line in f:
       #data.append( json.loads(line) )
       #data.append( line )
       db.maps.insert(json.loads(line))
    
    #try:
    #    data = json.loads(f.read())
    #except ValueError:
    #    pass
    print len(data)
    f.close()
    zf.close()

    
def get_data(db):
    return db.maps.find_one()

def get_db():
    # For local use
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    # 'examples' here is the database name. It will be created if it does not exist.
    db = client.examples
    return db

if __name__ == "__main__":
    # For local use
    db = get_db() 
    add_data(db)
    print get_data(db)