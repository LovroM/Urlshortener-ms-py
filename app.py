import re

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://USER:PASS@localhost/DB_NAME"
db = SQLAlchemy(app)


class ShortUrl(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String, nullable = False)
    
    def __init__(self, url):
        self.url = url
        
    
# A simple home route that renders index.html
@app.route("/")
def index():
    return render_template("index.html")


#  Creating a new short url.
#  (Path converter accepts slashes)

#  Then checks if the short url for this url already exists
#  in the database. If it does, it returns the existing one in json
#  format. If not, it creates a new one and return it's data.
@app.route("/new/<path:new_url>")
def new_link(new_url):
    
    http_valid_format = re.compile("(https?:\/\/\w+\.\w+.+)")
    # First checks if the inserted url matches a valid url format.
    if http_valid_format.match(new_url):
        
        new_short_url = ""
        
        return jsonify(original_url = new_url,
                       short_url = new_short_url)
                       
    # Else returns error.
    else:
        return jsonify(error="Wrong url format, make sure you \
                              have a valid protocol and a real site.")


# Route that accepts an int id that is supposed to be a short url 
@app.route("/<int:id>")
def get_link(id):
    # Check the databse for existing id and redirect : else return error
    return jsonify(error = "This url is not in the database.")


# Runs server
if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 8080)