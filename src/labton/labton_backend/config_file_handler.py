import yaml
import os
import pkg_resources

class ConfigHandler:
    def __init__(self,
                data_source=pkg_resources.resource_filename(
                    'labton', 'data/csv_text/labton_default_project.csv'),
                csv_sep = r"§",
                path_experiment="",
                classes=["Positive", "Negative", "Neutral", "Paradox"], 
                port=8080, 
                host='0.0.0.0',
                project_name = "labton_default_project",
                path_config_folder = "projects_config_files",
                path_db_folder = "projects_db_files",
                use_ngrok = False,
                ngrok_auth_token = None
                 ):
        
        self.config = {
            "data_source": data_source, 
            "csv_sep": csv_sep,
            "path_experiment": path_experiment,
            "path_config_folder": path_config_folder,
            "path_db_folder": path_db_folder,
            "config_file_name": f'{project_name}_config.yaml',
            "db_file_name": f'{project_name}.db',
            "classes": classes, 
            "port": port, 
            "host": host,
            "project_name": project_name,
            "use_ngrok": use_ngrok,
            "ngrok_auth_token": ngrok_auth_token
            }
        
        self.config["path_config_file"] = f"{self.config['path_config_folder']}"+\
                                            f"/{self.config['config_file_name']}"
                                            
        self.config["path_db_file"] = f"{os.getcwd()}"+\
                                        f"/{self.config['path_db_folder']}"+\
                                        f"/{self.config['db_file_name']}"
    
    def create_folders_if_not_exists(self):
        #Make folder for config files of different projects
        if not os.path.exists(self.config["path_config_folder"]):
            os.mkdir(self.config["path_config_folder"])
        #Make folder for .db files of different projects 
        if not os.path.exists(self.config["path_db_folder"]):
            os.mkdir(self.config["path_db_folder"])
    
    def ensure_config_file_exists(self):
        #OBS! maybe automate this same as create_database in return_app
        assert os.path.exists(self.config["path_config_file"]),\
            "there must be a config file at this location:\n "+\
            f"{self.config['path_config_file']}"+\
            "make sure the self.config dict is correct and run "+\
            "self.save_project_config before running app"
            
    def save_project_config(self):
        self.create_folders_if_not_exists()
        #TODO: see if existing yaml differs from ConfigHandler object 
        # configurations if so, prompt user to decide which one to keep
        with open(self.config['path_config_file'], "w+") as f:
            try:
                yaml.safe_dump([self.config], f)
            except yaml.YAMLError as exc:
                print("Write to YAML failed with the following error:")
                print(exc)
    
    def load_project_config(self):
        self.ensure_config_file_exists()
        with open(self.config['path_config_file'], "r") as f:
            try:
                self.config = yaml.safe_load(f)[0]
            except yaml.YAMLError as exc:
                print(exc)

