from flask import Flask, send_from_directory
from labton.labton_backend.action_handler import ActionHandler
from datetime import timedelta
from pathlib import Path
import sys
import os

class FlaskAnotaterPage():
    

################ VARIABLES - Move to yaml later ###################
app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)
app.config["SESSION_COOKIE_SAMESITE"] = 'Strict'

#Generate secret key and write to secret yaml:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# ===========================SQLite DB ===========================

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

@app.route('/review', methods=['GET', 'POST'])
def review():
    with ActionHandler() as AH:
        return(AH.action_flow_review())

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(png_path, filename, as_attachment=True)

def load_project_config():
    import yaml
    with open('config.yaml') as f:
        try:
            project_config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

def return_app(app=app, project_name="Test_project"):
    
    # project_name = "Test_project"
    # db_path = Path(f"labton/data/{project_name}.db")
    # png_path = Path("labton/data/png_docs")
    # here = Path(os.getcwd())
    # db_file_path = here/db_path
    # os.environ["SQLITE_CONN_STR"] = str(db_file_path)
    # print(db_file_path, file=sys.stderr)
    
    
    app.config["project_name"] = self.project_name
    
    app.config["sqlite_conn_str"] = Path(os.getcwd())/\
        f"labton/data/{app.config['project_name']}.db"
    
    if not os.path.exists(db_file_path):
        from labton.labton_backend.data_handler import DatabaseHandler
        with DatabaseHandler() as DH:
            DH.create_database()
    
    return(app)