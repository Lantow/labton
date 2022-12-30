from labton.labton_ui import flask_annotater_page
from labton.labton_backend.config_file_handler import ConfigHandler
from labton.labton_backend.data_handler import DatabaseHandler

from flask import Flask
from pyngrok import ngrok
from pandas import DataFrame
import sys
import os

class App(ConfigHandler):
    def __init__(self, **kwargs):
        #Only overwrite default kwargs that are not None
        kwargs = {k:v for k,v in kwargs.items() if v}
        super().__init__(**kwargs)
        if 'google.colab' in sys.modules:
            self.config["ngrok_auth_token"] = True
        
    def run(self):
        data_source = self.config["data_source"]
        is_df = False
        
        if isinstance(data_source, DataFrame):
            assert "paragraph_text" in data_source.columns,\
                "DataFrame must as a minimum contain the column 'paragraph_text'"
            self.config["data_source"] = "local_data_frame"
            is_df = True
        
        self.load_and_merge_project_config()    
        self.save_project_config()
        
        app = Flask(__name__)
        app.config.update(self.config)
        with app.app_context():
            if not os.path.exists(self.config["path_db_file"]):
                with DatabaseHandler() as DH:
                        DH.create_database(data_source, 
                                           self.config["csv_sep"],
                                           is_df=is_df)
        app = flask_annotater_page.return_app(
            project_name=self.config["project_name"])
        
        if self.config["use_ngrok"]:
            if not self.config["ngrok_auth_token"]:
                self.config["ngrok_auth_token"] = input(
                            "Paste ngrok authentication token. "
                            "Your token can be found here:\n"
                            "https://dashboard.ngrok.com/get-started/your-authtoken\n")
                
            ngrok.set_auth_token(self.config["ngrok_auth_token"])
            public_url = ngrok.connect(self.config["port"])
            print(f"To access internet facing app you can go to: {public_url}")
            
        app.run(debug=False,
                host=app.config["host"], 
                port=app.config["port"])
    
