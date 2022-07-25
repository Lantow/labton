from labton.labton_ui import flask_annotater_page
from labton.labton_backend.config_file_handler import ConfigHandler

class App(ConfigHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def run(self):
        self.save_project_config()
        app = flask_annotater_page.return_app(
            project_name=self.config["project_name"])
        app.run(debug=False, 
                host=app.config["host"], 
                port=app.config["port"])
        
