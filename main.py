from flask import Flask, current_app, jsonify, request, render_template
import os
import mysql.connector
import random
from math import radians, cos, sin, asin, sqrt
app = Flask(__name__)
def closest(n):
    return n[-1]

# function to sort the tuple
def sort(list_of_tuples):
    return sorted(list_of_tuples, key = closest)

def distance(lat1, lat2, lon1, lon2):

    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers (6371). Use 3956 for miles
    r = 3956

    # calculate the result
    return(c * r)



@app.route('/')
def index():
    return jsonify({"Geography Game API": "Welcome!"})

@app.route('/capitals_by_lat')
#-90 to 90
def capitals_by_lat():
    lat_from=request.args.get("lat_from", default="", type=str)
    lat_to=request.args.get("lat_to", default="", type=str)
    if(float(lat_from)<-90.0 or float(lat_to)>90.0):
        return(jsonify("Latitude outside range. Can only be between -90 and 90"))
    list_of_countries=[]
    cnx = mysql.connector.connect(user='root', database='railway', host='containers-us-west-30.railway.app', password='uRmUBE9EPeW2Q73NQWgm', port='6811')
    cursor = cnx.cursor()
    query = ("SELECT * FROM country")
    cursor.execute(query)
    for (test) in cursor:
      if(float(lat_from)<=float(test[3])<=float(lat_to)):
          list_of_countries.append(test)
    return(jsonify(sorted(list_of_countries)))

@app.route('/capitals_by_lon')
#-180 to 180
def capitals_by_lon():
    lon_from=request.args.get("lon_from", default="", type=str)
    lon_to=request.args.get("lon_to", default="", type=str)
    if(float(lon_from)<-180.0 or float(lon_to)>180.0):
        return(jsonify("Longitude outside range. Can only be between -180 and 180"))
    else:
        list_of_countries=[]
        cnx = mysql.connector.connect(user='root', database='railway', host='containers-us-west-30.railway.app', password='uRmUBE9EPeW2Q73NQWgm', port='6811')
        cursor = cnx.cursor()
        query = ("SELECT * FROM country")
        cursor.execute(query)
        for (test) in cursor:
          if(float(lon_from)<=float(test[4])<=float(lon_to)):
              list_of_countries.append(test)
        return(jsonify(sorted(list_of_countries)))


@app.route('/capitals')
def get_capitals():
    list_of_countries=[]
    cnx = mysql.connector.connect(user='root', database='railway', host='containers-us-west-30.railway.app', password='uRmUBE9EPeW2Q73NQWgm', port='6811')
    cursor = cnx.cursor()
    query = ("SELECT * FROM country")
    cursor.execute(query)
    for (test) in cursor:
      list_of_countries.append(test[2])
    return(jsonify(sorted(list_of_countries)))
@app.route('/countries')
def get_countries():
    list_of_countries=[]
    cnx = mysql.connector.connect(user='root', database='railway', host='containers-us-west-30.railway.app', password='uRmUBE9EPeW2Q73NQWgm', port='6811')
    cursor = cnx.cursor()
    query = ("SELECT * FROM country")
    cursor.execute(query)
    for (test) in cursor:
      list_of_countries.append(test[1])
    return(jsonify(sorted(list_of_countries)))

@app.route('/closest_capitals')
def get_closest_capitals():
    the_country=request.args.get("country", default="", type=str)
    num_results=request.args.get("results", default="", type=str)
    print(f"The Country is {the_country}")
    if(num_results==""):
        num_results=5
    if(num_results!=""):
        num_results=int(num_results)
    list_of_countries=[]

    cnx = mysql.connector.connect(user='root', database='railway', host='containers-us-west-30.railway.app', password='uRmUBE9EPeW2Q73NQWgm', port='6811')
    cursor = cnx.cursor()

    query = ("SELECT * FROM country")
    cursor.execute(query)
    for (test) in cursor:
      list_of_countries.append(test[1])
    if(the_country!=""):
        random_country=the_country
    if(the_country==""):
        random_country=random.choice(list_of_countries)
    query = (f"SELECT * FROM country WHERE country='{random_country}'")
    cursor.execute(query)
    country_from=None
    country_from_lat=None
    country_from_lon=None
    country_to=None
    country_to_lat=None
    country_to_lon=None
    for (test) in cursor:
      country_from_lat=test[3]
      country_from_lon=test[4]
      print(test)
    query = (f"SELECT * FROM country WHERE country!='{random_country}'")
    smallest=[]
    cursor.execute(query)
    for (test) in cursor:
      country_to_lat=test[3]
      country_to_lon=test[4]
      the_distance=distance(float(country_from_lat), float(country_to_lat), float(country_from_lon), float(country_to_lon))
      smallest.append((test,the_distance))
    sorted_list=sort(smallest)[:num_results]
    query = (f"SELECT * FROM country WHERE country='{random_country}'")
    cursor.execute(query)
    for (test) in cursor:
       sorted_list.insert(0,(test[1],test[2]))
    return (jsonify(sorted_list))



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
