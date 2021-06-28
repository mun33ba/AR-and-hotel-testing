from sqlalchemy import create_engine
import pyodbc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import join, intersect, union, update
from sqlalchemy.sql import select, intersect, union
import json
import os
from pathlib import Path
import urllib

Base = declarative_base()

path = os.getcwd()
path = Path(path)
config = "/".join(__file__.split("\\")[:-1])+"/config.json"
# config = str(path) + '/config.json'
config_json = config

class Hotels(Base):
    __tablename__ = 'Hotels'

    id = Column('Id', Integer, primary_key=True)
    name = Column("Name", String(50))
    address = Column('Address', String(255))
    city = Column('City', String(50))
    stars = Column('Stars', String(10))
    reviewCount = Column('Review Count', String(100))
    categories = Column('Categories', String(100))
    latitude = Column('Latitude', String(20))
    longitude = Column('Longitude', String(20))
    price = Column('Price', String(20))

class MySQL():
    def __init__(self):
        with open(str(config_json)) as config:
            conf = json.load(config)
            self.username = conf['database']['username']
            self.password = conf['database']['password']
        self.engine = create_engine(
            "mysql+pymysql://"+self.username+":"+self.password+"@localhost/hotels",
            echo=False)
        Base.metadata.create_all(bind=self.engine, checkfirst=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


    def getAllData(self):
       for data in self.session.query(Hotels).all():
            result = {
                "Name": data.id,
                "Address": data.address,
                "City": data.city,
                "Stars": data.stars,
                "Categories": data.categories,
                "Price": data.price
            }
            return result


    def getHotels(self, hotelIds):
        print(type(hotelIds))
        data = []
        for hotelId in hotelIds:
            results = self.session.query(Hotels).get(hotelId)
            print(type(results))
            # for res in results:
            hotel = {
                    "Name": results.name,
                    "Address": results.address,
                    "City": results.city,
                    "Stars": results.stars,
                    "Categories": results.categories,
                    "Price": results.price
                }
            data.append(hotel)
        return data
        # print(hotel)


if __name__ == '__main__':
    sql = MySQL()
    sql.getHotels(2)