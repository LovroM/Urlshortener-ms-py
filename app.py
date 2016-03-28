from flask import Flask, render_template, jsonify
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/new/<new_url>")
def new_link(new_url):
    
    http_valid_format = re.compile("(https?:\/\/\w+\.\w+.+)")
    ##Check if new url has a valid format, if passes, check if it's already in the database
    if http_valid_format.match(new_url):
        
        new_short_url = ""
        
        return jsonify(original_url = new_url, short_url = new_short_url)
    else:
        return jsonify(error = "Wrong url format, make sure you have a valid protocol and real site.")


@app.route("/<int:id>")
def get_link(id):
    ##Check the databse for existing id and redirect : else return error
    return jsonify(error = "This url is not in the database.")


### Runs server
if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 8080)