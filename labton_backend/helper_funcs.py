from functools import wraps
from labton_backend.data_handler import SQliteConnection

def with_sqlite_conn(f):
    """
    Wrapper to wrap around function that executes 
    SQLite code on the database whos path is defined 
    in the global variable db_file_path    

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

def update_history(session, sent_id):
    #Hvis det ikke er første annotering i sessionen
    if "annotation_history" in session:
        history = session["annotation_history"]
        current_id = sent_id #post["sent_id"]
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

def fecth_new_sent_id(session, post, move):
    # forwards_idx = idx+1 if idx else null (there is no newer)
    # end_idx = -1 
    # back = idx-1 if idx else Null (there are no older)
    # begining = 0
    history = session["annotation_history"]
    current_id = post["sent_id"]
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
        new_sent_id = history[idx]
        print(new_sent_id)
        return(new_sent_id)
    else: 
        print("_"*70)
        print("THERE IS NO HISTORY")