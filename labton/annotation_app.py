from labton.labton_ui import flask_annotater_page
from pathlib import Path
import yaml
import os

class App():
    def __init__(self, 
                 data_source="labton/data/csv_text/Test_project.csv",
                 path_experiment="", 
                 classes=["Positive", "Negative", "Neutral", "Paradox"], 
                 port=8080, host='0.0.0.0',
                 project_name = "Test_project"
                 ):
        
        self.data_source = data_source
        self.classes = classes
        self.port = port
        self.host = host
        self.project_name = project_name
                
        self.path_experiment = Path(path_experiment)
        self.path_config_folder = Path("projects_config_files")
        self.path_project_config = self.path_config_folder/\
                                f'{self.project_name}_config.yaml'
        
    def save_project_config(self):
        
        config = [{"data_source": self.data_source, 
                   "path_experiment":self.path_experiment,
                   "classes": self.classes, 
                   "port": self.port, "host": self.host,
                   "project_name": self.project_name}]
    
        if not os.path.exists(self.path_config_folder):
            os.mkdir(self.path_config_folder)
        
        with open(self.path_project_config, "w") as f:
            try:
                yaml.dump(config, f)
            except yaml.YAMLError as exc:
                print(exc)   
    
    def run(self):
        app = flask_annotater_page.return_app(
            project_name=self.project_name)
        app.run(host=self.host, port=self.port, debug=False)
    
self = App()