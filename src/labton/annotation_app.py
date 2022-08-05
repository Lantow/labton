from labton.labton_ui import flask_annotater_page
from labton.labton_backend.config_file_handler import ConfigHandler
from labton.labton_backend.data_handler import DatabaseHandler
from flask import Flask
from pandas import DataFrame
import os

class App(ConfigHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def run(self):
        data_source = self.config["data_source"]
        is_df = False
        
        if isinstance(data_source, DataFrame):
            assert "paragraph_text" in data_source.columns,\
                "DataFrame must as a minimum contain the column 'paragraph_text'"
            self.config["data_source"] = "local_data_frame"
            is_df = True

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
        app.run(debug=False, 
                host=app.config["host"], 
                port=app.config["port"])
        
