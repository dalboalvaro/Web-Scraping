
import sys
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Create the database in Mongo 
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():
    mars_data = mongo.db.collection.find_one()
    print("mars_data:")
    print(mars_data)
    #return "hello world"
    return render_template("index.html", mars = mars_data)

@app.route('/scrape')
def scrape():
    # Run the scrape function
    mars_storedata = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_storedata, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)