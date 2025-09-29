import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_cors import CORS

# Load the env
load_dotenv()

# Get the mapbox token
mb_pk_default = os.getenv("MAPBOX_DEFAULT_TOKEN")

# And the app location
url_host = os.getenv("URL_HOST")
port_app = int(os.getenv("PORT_APP"))

# Instance the backend and allow communication jic
app = Flask(__name__)
CORS(app)

# Homepage
@app.route("/", methods=["GET"])
def home():
    return render_template(
        "mapbox.html", 
        mb_pk_default=mb_pk_default
    )

def main():
    app.run(debug=True, host=url_host, port=port_app)

if __name__ == "__main__":
    main()
