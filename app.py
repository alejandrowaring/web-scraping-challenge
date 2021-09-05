#imports
from flask import Flask, render_template,redirect
import pymongo
import scrape_mars
#init
app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_dict = db.mars_dict.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_dict)


@app.route("/scrape")
def scrape():
  
    mars_dict = db.mars_dict
    mars_data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars_dict.update({}, mars_data, upsert=True)
    print(mars_data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
