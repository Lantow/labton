from labton.labton_ui import flask_annotater_page
from labton.labton_backend.config_file_handler import ConfigHandler

class App(ConfigHandler):
    def __init__(self):
        super().__init__()
    
    def run(self):
        self.save_project_config()
        app = flask_annotater_page.return_app()
        app.run(debug=False, 
                host=app.config["host"], 
                port=app.config["port"])
        
self = App()
self.run()