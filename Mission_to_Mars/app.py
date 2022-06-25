from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Home route
@app.route("/")
def index():
    mars_info = mongo.db.collection.find_one()

    # Return template
    return render_template("index.html", space = mars_info)

@app.route("/scrape")
def scraper():
    
    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update Mongo database using update and upsert
    mongo.db.collection.update_one({}, {"$set":mars_data}, upsert=True)

    # Redirect back to home
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)