import pandas as pd
import sys
sys.path.append("..")
from MongoDB.script import Mongodb

# db = Mongodb()

def readMongo(db):
    final_data = []
    cursor = db.find()
    entries = list(cursor)
    for count, index in enumerate(entries):
        index['longitude'] = index['hotel_location']['coordinates'][0]
        index['latitude'] = index['hotel_location']['coordinates'][1]
        del index['hotel_location']
        final_data.append(index)
    df = pd.DataFrame(final_data)
    if '_id':
        del df['_id']
    return df

# readMongo()