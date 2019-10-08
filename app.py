from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db


@app.route("/")
def index():
    collection = db.mars.find_one()
    return render_template("index.html", mars_data=collection)


@app.route("/scrape")
def scraper():
    collection = db.mars
    mars_data = scrape_mars.scrape()
    collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)