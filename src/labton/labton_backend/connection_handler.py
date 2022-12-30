import sqlite3
import os
from flask import current_app


class SQliteConnection(object):
    """automatic open and close"""    
    def __init__(self):
        self.conn = None 
        self.curr = None
        #OBS! using current_app.config prevents the user from accessing
        #two different projects in the same browser session - they need 
        #To open a new browser session (private window) for each project 
        self.config = current_app.config

    def __enter__(self):
        print(f"Opening connection to {self.config['path_db_file']}")
        self.conn = sqlite3.connect(self.config["path_db_file"])
        self.curr = self.conn.cursor()
        return self    
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection")
        if exc_tb is None or "Aborted by KeyboardInterrupt" in str(exc_val):
            print("Comitting")
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()
