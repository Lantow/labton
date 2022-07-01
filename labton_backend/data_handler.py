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

class DataBaseHandler(SQliteConnection):
    def __init__(self):
        super().__init__()
        
    def fetch_from_db(self, columns, table, conditions=None, one=False):
        #Conditions must be string
        if type(columns) == str: columns = [columns]
        #https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.row_factory
        conditions_sql = f"WHERE {conditions}" if conditions else ""
        self.conn.execute(f"""
            SELECT {", ".join(columns)} 
            FROM {table}
            {conditions_sql};
        """)
        out = conn.fetchall() if not one else c.fetchone()
        return(out) if out else (None, None)
    
    def add_annotation(self, values, table):
        #OBS! make naming convention of databasecolumns in english
            self.conn.execute(f"""
            UPDATE {table} SET 
                        korrekt_annotering = ?, 
                        hvem_annoterede = ?, 
                        udtræk = ?
            WHERE sent_id == ?;""", values)
    
