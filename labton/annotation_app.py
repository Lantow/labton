from labton.labton_ui import flask_annotater_page

class App():
    def __init__(self, 
                 data_source="labton/data/csv_text/Test_project.csv", 
                 classes=["Positive", "Negative", "Neutral", "Paradox"], 
                 port=8080, host='0.0.0.0'):
        self.data_source = data_source
        self.classes=["Positive", "Negative", "Neutral", "Paradox"]
        self.port = port
        self.host = host
    
    def control_if_path_and_create(self):
        pass

    def run(self):
        app = flask_annotater_page.return_app()
        app.run(host=self.host, port=self.port, debug=False)