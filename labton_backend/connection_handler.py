import sqlite3
import signal
import sys

class SQliteConnection(object):
    """automatic open and close"""    
    def __init__(self):
        self.conn = None 
        self.curr = None

    def _handle_interrupt(self, signum, frame):
        sys.exit("Aborted by KeyboardInterrupt") 

    def __enter__(self):
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)
        print("Opening connection")
        self.conn = sqlite3.connect(getenv('SQLITE_CONN_STR'))
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
