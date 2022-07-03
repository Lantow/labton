from flask import Flask, send_from_directory
from labton_backend.action_handler import ActionHandler

from datetime import timedelta
import sys
import os
from pathlib import Path

################ VARIABLES - Move to yaml later ###################
project_name = "Test_project"

##########################################

db_path = Path(f"data/{project_name}.db")
png_path = Path("data/png_docs")

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)
app.config["SESSION_COOKIE_SAMESITE"] = 'Strict'
# set the secret key. keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# ===========================SQLite DB ===========================
here = Path(os.getcwd())
db_file_path = here/db_path
os.environ["SQLITE_CONN_STR"] = str(db_file_path)
print(db_file_path, file=sys.stderr)

if not os.path.exists(db_file_path):
    from labton_backend.data_handler import DatabaseHandler
    with DatabaseHandler() as DH:
        DH.create_database()

@app.route('/', methods=["GET", 'POST'])
def annotering():
    with ActionHandler() as AH:
        return(AH.action_flow_annotation())
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    with ActionHandler() as AH:
        return(AH.action_flow_login())

@app.route('/logout')
def logout():
    with ActionHandler() as AH:
        return(AH.action_logout())

@app.route('/review')
def review():
    with ActionHandler() as AH:
        return(AH.action_flow_review())

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(png_path, filename, as_attachment=True)

def return_app(app=app):
    return(app)