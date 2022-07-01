from flask import Flask, session, render_template, request, redirect, url_for, jsonify, send_from_directory, abort
from labton_backend.data_handler import DataBaseHandler
from labton_backend.helper_funcs import update_history, fecth_new_sent_id

from simplepam import authenticate
from datetime import timedelta
from functools import wraps
import sqlite3
import sys
import os


DB = DataBaseHandler()

db_path = "/var/RAPID_PROTOTYPEING/DATA/UDLAND/db_data/TC_annotations.db"
png_path = "/var/RAPID_PROTOTYPEING/DATA/UDLAND/TC_Docouments/PNGDocuments"

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)
app.config["SESSION_COOKIE_SAMESITE"] = 'Strict'

# ===========================SQLite DB ===========================
here = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(here, db_path)
print(db_file_path, file=sys.stderr)

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
                
                sentlike, sent_id, pdf_name, page_nr = DB.fetch_from_db(["sentlike", "sent_id", "pdf_name", "page_nr"], "annotations", 
                                                            f"sent_id = {sent_id}" , one=True)
                if session["annotation_history"][-1] == sent_id:
                    session["history_dive"] = False
                print(f"ARE WE STILL DIVING?? {session['history_dive']}")
            
            else:
                print("STAYING IN THE FUTURE")
                sentlike, sent_id, pdf_name, page_nr = DB.fetch_from_db(["sentlike", "sent_id", "pdf_name", "page_nr"], "annotations", 
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

    sentlikes = DB.fetch_from_db(["sent_id", "sentlike", "korrekt_annotering", "udtræk"], "annotations",
                                "korrekt_annotering NOT NULL AND hvem_verificerede IS NULL " +\
                                f"AND hvem_annoterede <> '{session['username']}'", one=False)

    return render_template("review.html", enumerated_sentlikes = enumerate(sentlikes), total=len(sentlikes))


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(png_path, filename, as_attachment=True)

# set the secret key. keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def return_app(app=app):
    return(app)