from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/capitals')
def get_capitals():
    import mysql.connector
    list_of_countries=[]

    cnx = mysql.connector.connect(user='root', database='railway', host='containers-us-west-30.railway.app', password='uRmUBE9EPeW2Q73NQWgm', port='6811')
    cursor = cnx.cursor()

    import random
    query = ("SELECT * FROM country")
    cursor.execute(query) 
    for (test) in cursor:
      list_of_countries.append(test[2])
    return(jsonify(sorted(list_of_countries)))


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
