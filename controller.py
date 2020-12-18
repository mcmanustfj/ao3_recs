from flask import Flask, request, render_template, session
from tempfile import mkdtemp
from flask_session import Session
import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', -1)
import networkx as nx
from recomendation_engine.predictor import get_recs


app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route('/')
def my_form():
    if "rec" not in session:
        session["rec"] = None
    return render_template('view.html')

@app.route('/', methods=['POST'])
def my_form_post():
	session["fic_name"]=request.form['fic_name']
	rec_df=get_recs(session["fic_name"])
	session["recs"] = rec_df
	return render_template('view.html', fic_name=session["fic_name"],tables=[rec_df.to_html(classes='data', escape=False)],titles=rec_df.columns)
if __name__ == '__main__':
    app.run()
