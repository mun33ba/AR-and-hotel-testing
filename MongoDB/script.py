from pymongo import MongoClient, GEOSPHERE
import pprint
import os
import pandas as pd
from pathlib import Path
import json
import re

path = os.getcwd()
path = Path(path)
#config = "/".join(__file__.split("\\")[:-1])+"/config.json"
#config = str(path) + "/config.json"
#config_json = config
pattern = "^[0-9,;]+$"

class Mongodb:
    def __init__(self):
#        with open(str(config_json)) as config:
#            conf = json.load(config)
#            self.username = conf['database']['username']
#            self.password = conf['database']['password']
#            self.database = conf['database']['database']
        self.client = MongoClient("mongodb+srv://seyahat:muniba789@cluster0.6wv4j.mongodb.net/Seyahat?retryWrites=true&w=majority")
        self.db = self.client['Seyahat']
        self.col = self.db['Cluster0']


    def createIndex(self):
        self.col.create_index([("hotel_location", GEOSPHERE)])

    def info(self):
        self.client.server_info()

    def getCollectionNames(self):
        print(self.db.list_collection_names())


    def insertData(self, record):
        # dic = {
        #     "name": "Avari Towers Karachi",
        #     "address": "242-244 Fatima Jinnah Rd, Karachi Cantonment, Sindh 75530",
        #     "city": "Karachi",
        #     "stars": 4.4,
        #     "review_count": 8315,
        #     "categories": "Hotel",
        #     "price": 13671,
        #     "hotel_location": {
        #         "type": "Point",
        #         "coordinates": [
        #             67.0323, 24.8527
        #         ]
        #     }
        # }

        data = self.col.insert_one(record)
        print(data)

    def csvToDataFrame(self):
        df = pd.read_csv("../Data/final.csv").to_dict(orient='records')
        self.processEntries(df)


    def processEntries(self,dataframe):
        for count,index in enumerate(dataframe):
            coordinates = []
            coordinates.append(float(index['longitude']))
            coordinates.append(float(index['latitude']))
            del index['longitude']
            del index['latitude']
            res = re.findall(pattern,index['review_count'])
            if bool(res):
                index['review_count'] = index['review_count'].replace(',','')
            index['hotel_location'] = {
                "type": "Point",
                "coordinates": coordinates
            }
            if index['price'] != '':
                res = re.search(pattern, str(index['price']))
                if bool(res):
                    index['price'] = index['price'].replace(',','')
                else:
                    index['price'] = None
            self.insertData(index)


    def query(self,long,lat):
        hotels = []
        for doc in self.col.find({"hotel_location": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [long, lat]
                },
                "$maxDistance": 2500}}}):
            # new_doc = {
            #     "id": doc['id'],
            #     "hotel_location": doc["hotel_location"]
            # }
            del doc['_id']
            hotels.append(doc)
        # print(hotels)
        return hotels

if __name__ == "__main__":
    db = Mongodb()
    #db.csvToDataFrame()
    #db.insertData()
    #db.createIndex()
    #db.info()
    print(db.query(67.0323, 24.8526))
    db.getCollectionNames()
