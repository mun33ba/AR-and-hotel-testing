from MongoDB.script import Mongodb
from flask import Flask, jsonify, request, redirect, render_template, url_for
from geopy.geocoders import Nominatim

mongoDb = Mongodb()

app = Flask(__name__)
# app.add_url_rule(
#     '/graphql',
#     view_func=GraphQLView.as_view(
#         'graphql',
#         schema=schema,
#         graphiql=True
#         # context = {'session': mySQL.session}
#     )
# )
app.config['MONGODB_SETTINGS'] = {'db':'hotel', 'alias':'default'}

@app.route('/', methods=["POST","GET"])
def main_page():
    if request.method == "POST":
        address = request.form["from"]
        print(address)
        location = Nominatim(user_agent='test').geocode(address)
        lng = location.longitude
        lat = location.latitude
        return redirect(url_for("hotelLocations", longitude=lng, latitude=lat))
    else:
        return render_template("recommendationui.html")

@app.route('/read/<longitude>,<latitude>')
def hotelLocations(longitude,latitude):
    print(type(longitude), type(latitude))
    res = mongoDb.query(float(longitude),float(latitude))
    # hotels = mySQL.getHotels(res)
    return jsonify({"hotels": res})



if __name__ == '__main__':
    app.run(port=5011,debug=True)