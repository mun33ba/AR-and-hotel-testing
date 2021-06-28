import pprint
from bson.json_util import loads
def query(db):
    hotels = []
    for doc in db.find({"hotel_location": {
        "$nearSphere": {
            "$geometry": {
                "type": "Point",
                "coordinates": [67.1234478, 24.9296513]
            },
            "$maxDistance": 5000}}}):
        new_doc = {
            "id": doc['id'],
            "hotel_location": doc["hotel_location"]
        }
        hotels.append(new_doc)
    print(hotels)
    return hotels