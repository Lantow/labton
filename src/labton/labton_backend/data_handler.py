from labton.labton_backend.connection_handler import SQliteConnection
import pandas as pd


class DatabaseHandler(SQliteConnection):
    def __init__(self):
        super().__init__()
        
    def create_database(self, data_source, csv_sep, is_df=False):
        if is_df:
            df_text = data_source
        else:
            df_text = pd.read_csv(data_source, 
                                sep=csv_sep, keep_default_na=False,
                                engine='python', skipinitialspace=True,
                                names=["paragraph_text", "document_name", "page_nr"])
        df_text["paragraph_id"] = df_text.index
        df_text.to_sql(name = "annotations", con = self.conn)
        columns_to_add = [
                            "correct_annotation CHAR(50)",
                            "who_annotated CHAR(50)",
                            "extract VARCHAR(10)",
                            "who_verified CHAR(50)",
                            "verification CHAR(50)"
                        ]
        
        add_col = lambda col:  self.conn.execute(f"ALTER TABLE annotations ADD {col}")
        for col in columns_to_add: add_col(col)     
    
    def fetch_from_db(self, columns, table, conditions=None, one=False):
        #Conditions must be string
        if type(columns) == str: columns = [columns]
        #https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.row_factory
        conditions_sql = f"WHERE {conditions}" if conditions else ""
        self.curr.execute(f"""
            SELECT {", ".join(columns)} 
            FROM {table}
            {conditions_sql};
        """)
        out = self.curr.fetchall() if not one else self.curr.fetchone()
        return(out) if out else (None, None, None, None)
    
    def add_annotation(self, values, table):
        #OBS! make naming convention of databasecolumns in english
        self.conn.execute(f"""
        UPDATE {table} SET 
                    correct_annotation = ?, 
                    who_annotated = ?, 
                    extract = ?
        WHERE paragraph_id == ?;""", values)
    
    def verify_annotation(self, values, table):
        self.conn.execute(f"""
        UPDATE {table} SET 
                    who_verified = ?,
                    verification = ? 
        WHERE paragraph_id == ?;
        """, values)

    def load_annotations_to_pandas(self):
        return(pd.read_sql("SELECT * FROM annotations", self.conn))