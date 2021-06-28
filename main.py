#from MySQL.database import MySQL
from MongoDB.script import Mongodb
from MongoDB.mongo import query
from flask import Flask, render_template,jsonify, request, redirect, Response
from flask_pymongo import PyMongo
import json, bson
#from flask_graphql import GraphQLView
#from GraphQL.mongo_schema import schema

mongoDb = Mongodb()
# mySQL = MySQL()

app = Flask(__name__)
# app.add_url_rule(
#     '/graphql',
#     view_func=GraphQLView.as_view(
#         'graphql',
#         schema=schema,
        
#         # context = {'session': mySQL.session}
#     )
# )
app.config['MONGODB_SETTINGS'] = {'db':'Cluster0', 'alias':'default'}

# app.config["MONGO_URI"] = "mongodb+srv://user:Linkedlist22@cluster0.dhero.mongodb.net/Hotels?retryWrites=true&w=majority"
# mongo = PyMongo(app)
# db_operations = mongo.db.hotel
# print(db_operations)

@app.route('/')
def home():
    return render_template('recommendationui.html')
   # return "Hello World"

@app.route('/read')
def hotelLocations():
    res = mongoDb.query(67.0323, 24.8526)
    # hotels = mySQL.getHotels(res)
    return jsonify({"hotels": res})


if __name__ == '__main__':
    app.run(port=5011,debug=True)