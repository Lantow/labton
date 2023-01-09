from labton.backend.data_handler import DatabaseHandler
from labton.backend.helper_funcs import update_history, fecth_new_paragraph_id
from flask import session, render_template, request, redirect, url_for, jsonify, send_from_directory, abort

class ActionHandler(DatabaseHandler):
    def __init__(self):
        super().__init__()
        
    def action_flow_annotation(self):
        if 'username' in session:
                
                if request.method == 'POST':
                    post = request.get_json()
                    if post["action"] == "annotate":
                        values = [post["annotation"],session["username"], 
                                post["annotering_text"].strip() if post["annotering_text"] else None,
                                post["paragraph_id"]]
                        self.add_annotation(values, "annotations")

                    elif post["action"] == "review":
                        #https://stackoverflow.com/questions/15473626/make-a-post-request-while-redirecting-in-flask/15480983#15480983
                        return redirect(url_for('review'))

                    elif post["action"] == "logout":
                        #Save and close user_session table
                        session.clear()
                        return redirect(url_for('login'))

                    elif post["action"] in ["back", "begining", "forward", "end"]:
                        paragraph_id = fecth_new_paragraph_id(session, post, post["action"])
                        history_dive = True

                    else:
                        pass

                #Hvis session stadig er aktiv og der  ikke er er defieneret et paragraph_id 
                # (dette sker hvis man har lukket browser og er logget ind igen)
                #Så hent sidste entry i annotation_history som paragraph_id
                try: paragraph_id
                except NameError: 
                    if "history_dive" in session: 
                        paragraph_id = session["annotation_history"][-1]
                    else: pass
                
                dive_check = session["history_dive"] if "history_dive" in session else False
                #Hvis man er på den nyeste sætning, så er man ude af historie dykket
                #OBS! herved vil man aldrig lande på den sidste sætning igen :/ må løses
                if "history_dive" in session and session["history_dive"] is True:                    
                    text, paragraph_id, id1, id2 = self.fetch_from_db(["text", 
                                                    "paragraph_id", "id1", "id2"], "annotations", 
                                                    f"paragraph_id = {paragraph_id}" , one=True)
                    if session["annotation_history"][-1] == paragraph_id:
                        session["history_dive"] = False
                else:               
                    text, paragraph_id, id1, id2 = self.fetch_from_db(["text", 
                                                                    "paragraph_id", "id1", "id2"], 
                                                                    "annotations", "correct_annotation IS null", 
                                                                    one=True)
                update_history(session, paragraph_id)
                return render_template("annotering.html", 
                                        session=session,
                                        sent=text,
                                        paragraph_id=paragraph_id,
                                        png_name= f"{id1}000{id2}-{id2}.png",
                                        classes=self.config["classes"])
        else:
            return redirect(url_for('login'))

    def action_flow_login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            #TODO: implement login here
            if username: #authenticate(str(username), str(password))
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
                    <h2>You need to type in a name to annotate as<h2>
                    <form action="/login">
                            <input type="submit" value="Try again" />
                    </form> 
                """
                'Invalid username/password'
        else:
            return render_template("login.html")
    
    def action_logout(self):
        # remove the username from the session if it's there
        session.pop('username', None)
        return redirect(url_for('annotering'))
    
    def action_flow_review(self):
        if 'username' in session:
            if request.method == 'POST':
                post = request.get_json()
                if post["action"] == "submit":
                    paragraph_ids = post["paragraph_ids"] 
                    who_verified = post["who_verified"]
                    verifications = post["verifications"]
                    for values in zip(who_verified, verifications, paragraph_ids):
                        self.verify_annotation(values, "annotations")
            
            annotated_texts = self.fetch_from_db(["paragraph_id", "text", "correct_annotation", "extract"], "annotations",
                                        "correct_annotation NOT NULL AND who_verified IS NULL " +\
                                        f"AND who_annotated <> '{session['username']}'", one=False)
            #OBS! DataHandler.fetch_from_db returns (None, None, None, None) when nothing found in DB
            #We avoid empty lines in the reviewpage with the following line of code
            annotated_texts =  [i for i in annotated_texts if i]
            return render_template("review.html", enumerated_annotated_texts = enumerate(annotated_texts), 
                                                        total=len(annotated_texts), session=session)
        else:
            return redirect(url_for('login'))