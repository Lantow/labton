from labton_backend.helper_funcs import with_sqlite_conn

class DatabaseHandler:
    def __init__(self):
        pass
    
    @with_sqlite_conn
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
    
    @with_sqlite_conn
    def add_annotation(self, values, table):
        #OBS! make naming convention of databasecolumns in english
        self.conn.execute(f"""
        UPDATE {table} SET 
                    korrekt_annotering = ?, 
                    hvem_annoterede = ?, 
                    udtræk = ?
        WHERE sent_id == ?;""", values)
    
    @with_sqlite_conn
    def verify_annotation(self, values, table):
        self.conn.execute(f"""
        UPDATE {table} SET 
                    hvem_verificerede = ?,
                    verifikation = ? 
        WHERE sent_id == ?;
        """, values)
