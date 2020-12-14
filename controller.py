from flask import Flask, request, render_template, session
from tempfile import mkdtemp
from flask_session import Session
import numpy as np
import pandas as pd

from recomendation_engine.predictor import get_top_rec
app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

df = pd.DataFrame({'name': ["fic1", "fic2", "fic3"],
                   'url': ["url1", "url2", "url3"],
                   'percent_of_users_who_liked_it': [0.3, 0.2, 0.1]})

@app.route('/')
def my_form():
    if "rec" not in session:
        session["rec"] = None
    return render_template('view.html', rec=session["rec"], tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/', methods=['POST'])
def my_form_post():
	session["fic_name"]=request.form['fic_name']
	rec=get_top_rec(session["fic_name"])
	session["rec"] = rec
	return render_template('view.html', fic_name=session["fic_name"], rec=session["rec"],tables=[df.to_html(classes='data')], titles=df.columns.values)
