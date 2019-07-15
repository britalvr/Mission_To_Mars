from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
from Mars_Scrape import scrape


app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = pymongo(app)

mars_doc = scrape()
mars_db = client.mars_db
mars_db.Mission_To_Mars.drop()
mars_db.Mssion_To_Mars.insert(mars_doc)


# mongo = pymongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    # mars_doc = mongo.db.mars.find()
    # return render_template("index.html", mars = mars_doc)
    mars_doc = mars_db.Mission_To_Mars.find()
    return render_template("index.html", mars = mars_doc)


@app.route("/scrape")
def scraper():    
    mars_doc = scrape()
    mars_db = client.Mars_db
    mars_db.Mission_To_Mars.drop()
    mars_db.Mission_To_Mars.insert(mars_doc)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug = True)