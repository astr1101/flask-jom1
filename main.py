from flask import Flask, current_app, jsonify, request, render_template
import os
import mysql.connector
import random
from math import radians, cos, sin, asin, sqrt
app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/capitals')
def get_capitals():
    
    list_of_countries=[]

    cnx = mysql.connector.connect(user='root', database='railway', host='containers-us-west-30.railway.app', password='uRmUBE9EPeW2Q73NQWgm', port='6811')
    cursor = cnx.cursor()

    import random
    query = ("SELECT * FROM country")
    cursor.execute(query) 
    for (test) in cursor:
      list_of_countries.append(test[2])
    return(jsonify(sorted(list_of_countries)))

@app.route('/closest_capitals')
def get_closest_capitals():
    #5 Closest Country Capitals to a Random Country in KM
#/closest_capitals/random?results=5
#/closest_capitals/?country=&results=1
    the_country=request.args.get("country", default="", type=str)
    num_results=request.args.get("results", default="", type=str)
    if(num_results==""):
        num_results=5
    if(num_results!=""):
        num_results=int(num_results)
    list_of_countries=[]

    cnx = mysql.connector.connect(user='root', database='railway', host='containers-us-west-30.railway.app', password='uRmUBE9EPeW2Q73NQWgm', port='6811')
    cursor = cnx.cursor()
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

        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371

        # calculate the result
        return(c * r)

    
    query = ("SELECT * FROM country")
    cursor.execute(query) 
    for (test) in cursor:
      list_of_countries.append(test[1])

    random_country=random.choice(list_of_countries)
    print(random_country)
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
      #print(test_2)
    #print((sort(smallest)[0][0][1],sort(smallest)[0][0][2], sort(smallest)[0][1]))
    #print((sort(smallest)[1][0][1],sort(smallest)[1][0][2], sort(smallest)[1][1]))
    #print((sort(smallest)[2][0][1],sort(smallest)[2][0][2], sort(smallest)[2][1]))
    #print((sort(smallest)[3][0][1],sort(smallest)[3][0][2], sort(smallest)[3][1]))
    #print((sort(smallest)[4][0][1],sort(smallest)[4][0][2], sort(smallest)[4][1]))
    query = (f"SELECT * FROM country WHERE country='{random_country}'")
    cursor.execute(query)
    for (test) in cursor:   
        smallest.prepend(test[1],test[2])
    print(sort(smallest)[:num_results])
    return (jsonify(sort(smallest)[:num_results]))



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
