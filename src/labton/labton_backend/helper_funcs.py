from functools import wraps
from flask import Flask
from pandas import DataFrame
from labton.labton_backend.connection_handler import SQliteConnection
from labton.labton_backend.config_file_handler import ConfigHandler
from labton.labton_backend.data_handler import DatabaseHandler

def with_sqlite_conn(f):
    """
    Wrapper to wrap around function that executes 
    SQLite code on the database whos path is defined 
    in the config variable path_db_file

    Args:
        f (function): function that excecutes to SQL-db
    Returns:
        function: function wrapped such that 
                open/close/commit is handeled automatically
    """
    @wraps(f)
    def wrapper(*args, **kwds):
        with SQliteConnection() as conn_obj:
            return f(*args, conn=conn_obj.conn, curr=conn_obj.curr, **kwds)
    return wrapper

def update_history(session, paragraph_id):
    #Hvis det ikke er første annotering i sessionen
    if "annotation_history" in session:
        history = session["annotation_history"]
        current_id = paragraph_id #post["paragraph_id"]
        #Hvis annoterede sætning allerede er blevet annoteret
        if current_id not in history:
            history += [current_id]
            session["annotation_history"] = history
        else:
            pass
            # idx = history.index(current_id) 
            # del history[idx]

    else: 
        session["annotation_history"] = []
    print(session["annotation_history"])
    return session

def fecth_new_paragraph_id(session, post, move):
    # forwards_idx = idx+1 if idx else null (there is no newer)
    # end_idx = -1 
    # back = idx-1 if idx else Null (there are no older)
    # begining = 0
    history = session["annotation_history"]
    current_id = post["paragraph_id"]
    session["history_dive"] = True
    if history:
        # print(history)
        #Hvis sætningen er del af sæssions historien
        #Altså hvis det er en sætning, der har været set på før
        idx = history.index(current_id) if current_id in history else -1

        #Remember the frontend screens for errors like at the end or begining of list
        if idx != -1:
            if move == "forward":
                idx += 1
            elif move == "back":
                idx -= 1
            elif move == "end":
                pass
            elif move == "begining":
                pass
        print("HISTORY")
        print(history)
        print("INDEX")
        print(idx)
        new_paragraph_id = history[idx]
        print(new_paragraph_id)
        return(new_paragraph_id)
    else: 
        print("_"*70)
        print("THERE IS NO HISTORY")
        
def create_dataframe_template():
    return(DataFrame(columns=["paragraph_text", "document_name", "page_nr"]))
    
def get_labton_data(project_name="labton_default_project"):
    app = Flask(__name__)
    ch = ConfigHandler(project_name=project_name)
    ch.load_and_merge_project_config()
    app.config.update(ch.config)
    with app.app_context():
        with DatabaseHandler() as DH:
            return(DH.load_annotations_to_pandas())