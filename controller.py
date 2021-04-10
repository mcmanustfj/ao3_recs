from tempfile import mkdtemp

import pandas as pd

from flask import Flask, render_template, request, session
from flask_session import Session
from recomendation_engine.predictor import get_recs

pd.set_option('display.max_colwidth', None)

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
    fic_name, rec_df = get_recs(request.form['fic_name'], 20)
    session["fic_name"] = fic_name
    session["recs"] = rec_df
    return render_template('view.html', fic_name=session["fic_name"],
                           tables=[rec_df.to_html(classes='data', escape=False)], titles=rec_df.columns)


if __name__ == '__main__':
    app.run()
