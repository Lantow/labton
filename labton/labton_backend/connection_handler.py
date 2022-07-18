import sqlite3
import os

class SQliteConnection(object):
    """automatic open and close"""    
    def __init__(self):
        self.conn = None 
        self.curr = None
        self.db_file_path = os.getenv('SQLITE_CONN_STR')

    def __enter__(self):
        print("Opening connection")
        self.conn = sqlite3.connect(self.db_file_path)
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
