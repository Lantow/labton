from flask import Flask, session, render_template, request, redirect, url_for, jsonify, send_from_directory, abort
from flask_login import LoginManager

from simplepam import authenticate
from datetime import timedelta
from functools import wraps
import sqlite3
import sys
import os

db_path = "/var/RAPID_PROTOTYPEING/DATA/UDLAND/db_data/TC_annotations.db"
png_path = "/var/RAPID_PROTOTYPEING/DATA/UDLAND/TC_Docouments/PNGDocuments"

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)
app.config["SESSION_COOKIE_SAMESITE"] = 'Strict'
login_manager = LoginManager()
login_manager.init(app)
# ===========================SQLite DB ===========================
here = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(here, db_path)
print(db_file_path, file=sys.stderr)

def create_connection(f):
    wraps(f)
    def wrapped(*args, **kwargs):
        try:
            with sqlite3.connect(db_file_path) as conn:
               # conn.row_factory = lambda cursor, row: row[0]    
                c = conn.cursor()
                out = f(c, *args, **kwargs)
                c.close()
                conn.commit
                return out
        except sqlite3.Error as e:
            print(e, file=sys.stderr)
    return(wrapped)

@create_connection
def fetch_from_db(c, columns, table, conditions=None, one=False):
    #Conditions must be string
    if type(columns) == str: columns = [columns]
    #https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.row_factory
    conditions_sql = f"WHERE {conditions}" if conditions else ""
    c.execute(f"""
        SELECT {", ".join(columns)} 
        FROM {table}
        {conditions_sql};
    """)
    out = c.fetchall() if not one else c.fetchone()
    return(out) if out else (None, None)

@create_connection
def add_annotation(c, values, table):
    c.execute(f"""
        UPDATE {table} SET 
                    korrekt_annotering = ?, 
                    hvem_annoterede = ?, 
                    udtræk = ?
        WHERE sent_id == ?;
    """, values)

# ==================== HELPER FUNCS =======================
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
# =========================================================

# c = conn.cursor()
# c.execute(f"""SELECT sent FROM SENTs where annotering is null;""")
# c.fetchone()

@app.route('/', methods=["GET", 'POST'])
def annotering():
        if 'username' in session:
            print("_"*70)
            
            if request.method == 'POST':
                print("*"*70)
                post = request.get_json()
                print("POST:")
                print(post, end="\n")
                if post["action"] == "annotate":
                    values = [post["annotation"],session["username"], 
                              post["annotering_text"].strip() if post["annotering_text"] else None,
                              post["sent_id"]]
                    add_annotation(values, "annotations")
                    print(session)

                elif post["action"] == "review":
                    print("||"*70)
                    print("THIS IS REVIEW")
                    return redirect(url_for('review'))

                elif post["action"] == "logout":
                    #Save and close user_session table
                    session.clear()
                    return redirect(url_for('login'))

                elif post["action"] in ["back", "begining", "forward", "end"]:
                    print("BUTTON PRESSED")
                    sent_id = fecth_new_sent_id(session, post, post["action"])
                    history_dive = True

                else:
                    pass

            #Hvis session stadig er aktiv og der ikke er er defieneret et sent_id 
            # (dette sker hvis man har lukket browser og er logget ind igen)
            #Så hent sidste entry i annotation_history som sent_id
            try: sent_id
            except NameError: 
                if "history_dive" in session: 
                    sent_id = session["annotation_history"][-1]
                else: pass
            
            dive_check = session["history_dive"] if "history_dive" in session else False
            print(f"ARE WE DIVING?? {dive_check}")
            #Hvis man er på den nyeste sætning, så er man ude af historie dykket
            #OBS! herved vil man aldrig lande på den sidste sætning igen :/ må løses
            if "history_dive" in session and session["history_dive"] is True:
                print("GOING TO THE PAST")
                
                sentlike, sent_id, pdf_name, page_nr = fetch_from_db(["sentlike", "sent_id", "pdf_name", "page_nr"], "annotations", 
                                                            f"sent_id = {sent_id}" , one=True)
                if session["annotation_history"][-1] == sent_id:
                    session["history_dive"] = False
                print(f"ARE WE STILL DIVING?? {session['history_dive']}")
            
            else:
                print("STAYING IN THE FUTURE")
                sentlike, sent_id, pdf_name, page_nr = fetch_from_db(["sentlike", "sent_id", "pdf_name", "page_nr"], "annotations", 
                                                            "korrekt_annotering IS null and regex_annotering = 1" , one=True)
            print("SENT SUPPOSED TO BE ON SCREEN")
            print(sentlike)
            update_history(session, sent_id)
            return render_template("annotering.html", 
                                    session=session,
                                    sent=sentlike,
                                    sent_id=sent_id,
                                    png_name= f"{pdf_name}000{page_nr}-{page_nr}.png",
                                    classes=["UGELØN", "ÅRSLØN", "MÅNEDSLØN", "TIMELØN", "SLUTDATO", 
                                            "STARTDATO", "CVR", "TELEFONNR", "INTET", "TVETYDIG"])
        else:
            return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(str(username), str(password)):
            session['username'] = request.form['username']
            return redirect(url_for('annotering'))
        else:
            return """
                <head>
                <style type="text/css">
                    body {
                    text-align: center;
                    background-size: 100%;
                    }
                    h1, h2 {
                    color: black;
                    font-family: "Courier New";
                    }
                </style>
                </head>
                <h2>Forkert kode indtastet - <br> Hændelsen er logført<h2>
                <form action="/login">
                        <input type="submit" value="Prøv igen" />
                </form>
            """
            'Invalid username/password'
    return render_template("login.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('annotering'))

@app.route('/review')
def review():
    #TODO: IMPLEMENTER EN MÅDE AT RETTE I FOREGÅENDE INDTASTNINGER
    #F.EKS VED AT HAVE EN LISTE OVER INDTASTNINGER SIDEN SESSIONENS START
    # ELLER VED AT HAVE EN ENDELIG SIDE, HVOR COMMITS KAN LAVES TIL DEN 
    # ENDELIGE DATA BASE

    sentlikes = fetch_from_db(["sent_id", "sentlike", "korrekt_annotering", "udtræk"], "annotations",
                                "korrekt_annotering NOT NULL AND hvem_verificerede IS NULL " +\
                                f"AND hvem_annoterede <> '{session['username']}'", one=False)

    return render_template("review.html", enumerated_sentlikes = enumerate(sentlikes), total=len(sentlikes))


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(png_path, filename, as_attachment=True)

# set the secret key. keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug='True')