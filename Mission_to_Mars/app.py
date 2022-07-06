from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

# Instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Home route
@app.route("/")
def index():
    mars_info = mongo.db.collection.find_one()

    # Return template
    return render_template("index.html", mars_info = mars_info)

@app.route("/scrape")
def scraper():

    mars_info = mongo.db.collection
    
    # Run the scrape function
    mars_data = scrape.scrape_info()

    # Update Mongo database using update and upsert
    # mars_info.update_one({}, {"$set":mars_data}, upsert=True)
    mars_info.insert_one(mars_data)

    # Redirect back to home
    return redirect("/",code=302)


if __name__ == "__main__":
    app.run(debug=True)