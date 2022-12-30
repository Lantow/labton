from labton.annotation_app import App
import argparse

#Parse argument to get project name
parser = argparse.ArgumentParser()
parser.add_argument("project_name", 
                    help="Name of the project. If the project does not exist, it will be created", 
                    nargs='?',
                    default='labton_default_project')
parser.add_argument("--data_source", 
                    help="Path to data source. If no path is given, the database will be created empty.")
parser.add_argument("--csv_sep", 
                    help="If data source is a csv file, the csv separator can be specified here. Default is ';'.")
parser.add_argument("--use_ngrok", 
                    help="If you want to access your app from the internet, you can use ngrok. "
                         "This argument will start ngrok and print the public url in the console. "
                         "You can also set this argument to False if you do not want to use ngrok. "
                         "Default is True.")
parser.add_argument("--port", 
                    help="Port to run the app on. Default is 5000.")
parser.add_argument("--ngrok_auth_token", 
                    help="If you want to use ngrok, you need to provide your ngrok authentication token. "
                         "Your token can be found here: https://dashboard.ngrok.com/get-started/your-authtoken. "
                         "If you do not want to use ngrok, you can set this argument to False.")

if __name__ == '__main__':
    args = parser.parse_args()
    app = App(project_name=args.project_name,
          data_source=args.data_source,
          csv_sep=args.csv_sep,
          use_ngrok=args.use_ngrok,
          port=args.port,
          ngrok_auth_token=args.ngrok_auth_token)
    app.run()