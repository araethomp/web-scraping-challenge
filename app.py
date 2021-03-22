from flask import Flask, render_template, redirect
from flask_pymongo import Pymongo
import scrape_mars

# Flask instance
app = Flask(__name__)

# MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# App routes

@app.route("/")
def index():
    mars = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars=mars_dict)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.replace_one({}, mars_data, upsert=True)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)