from flask import Flask, send_from_directory
from labton.labton_backend.action_handler import ActionHandler
from labton.labton_backend.config_file_handler import ConfigHandler
from labton.labton_backend.data_handler import DatabaseHandler
from datetime import timedelta
import sys
import os

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config["SESSION_COOKIE_SAMESITE"] = 'Strict'
# set the secret key. keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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
    return send_from_directory(path_png, filename, as_attachment=True)

def create_db_if_not_exists(app):
    with app.app_context():
        if not os.path.exists(app.config["path_db_file"]):
            with DatabaseHandler() as DH:
                    DH.create_database(app.config["data_source"], 
                                       app.config["csv_sep"])

def return_app(app=app, project_name="labton_default_project"):
    ch = ConfigHandler(project_name=project_name)
    ch.load_and_merge_project_config()
    app.config.update(ch.config)
    #create_db_if_not_exists(app)
    return(app)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runs app for annotation of text')
    parser.add_argument('project_name', type=str, 
                        help='Name of project mapping to the yaml config files')
    args = parser.parse_args()
    project_name = args['project_name']
