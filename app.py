import re

from flask import Flask, render_template, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jilimbqdchsyqh:XFLKG4A-rhWtDUnZBLhq-6lWSg@ec2-54-225-197-143.compute-1.amazonaws.com:5432/d704u3v0mlnj1"

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


#  Create a new short url.
#  (Used 'path' converter because it accepts slashes)
@app.route("/new/<path:new_url>")
def new_link(new_url):
    
    # To be changed when I know the heroku url path.
    APP_PATH = "urlshortener-ms-py.herokuapp.com/"
    
    http_valid_format = re.compile("(https?:\/\/\w+\.\w+.+)")
    # First checks if the inserted url matches a valid url format.
    if http_valid_format.match(new_url):
        
        # Then checks if the short url for this url already exists.
        temp_item = check_db_url(new_url)
        if temp_item:
    
            # If it does, returns the already existing one from the db.
            return jsonify(original_url=new_url,
                           short_url=APP_PATH+str(temp_item.id))
   
        else:
            
            # Else creates a new one.
            new_short_url = ShortUrl(new_url)
            db.session.add(new_short_url)
            db.session.commit()
            temp_item = check_db_url(new_url)
            return jsonify(original_url=new_url,
                           short_url=APP_PATH+str(temp_item.id))
    
    else:
    
        # Else returns error.
        return jsonify(error="Wrong url format, make sure you \
                              have a valid protocol and a real site.")


# Route that accepts an int id that is supposed to be a short url. 
@app.route("/<int:id>")
def get_link(id):
    
    # Check the databse for existing id.
    temp_item = ShortUrl.query.get(id)
    if temp_item:
        return redirect(temp_item.url, code=302)
    else:
        return jsonify(error = "This url is not in the database.")


# Checks the database for specific url.
def check_db_url(url):
    return ShortUrl.query.filter_by(url=url).first()
    

# Runs server.
if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 8080)