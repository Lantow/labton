from flask import Flask, send_from_directory
from labton_backend.action_handler import ActionHandler

from datetime import timedelta
import sys
import os

AH = ActionHandler()

db_path = "/var/RAPID_PROTOTYPEING/DATA/UDLAND/db_data/TC_annotations.db"
png_path = "/var/RAPID_PROTOTYPEING/DATA/UDLAND/TC_Docouments/PNGDocuments"

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)
app.config["SESSION_COOKIE_SAMESITE"] = 'Strict'
# set the secret key. keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# ===========================SQLite DB ===========================
here = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(here, db_path)
os.environ["SQLITE_CONN_STR"] = db_file_path
print(db_file_path, file=sys.stderr)

@app.route('/', methods=["GET", 'POST'])
def annotering():
    return(AH.action_flow_annotation())
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    return(AH.action_flow_login())

@app.route('/logout')
def logout():
    return(AH.action_logout())

@app.route('/review')
def review():
    return(AH.action_flow_review())

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(png_path, filename, as_attachment=True)

def return_app(app=app):
    return(app)