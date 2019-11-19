from flask import Flask, request, render_template, redirect, url_for, abort
from flask_json import FlaskJSON, JsonError, json_response, as_json

import util

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('ranking'))

@app.route('/upload', methods=['POST'])
def do_upload():
    upload = request.files.get('upload', '')
    if not upload.filename.lower().endswith(('.csv')):#TODO verfy RIGHT WAY
        raise JsonError(description="Invalid file.")
    try:
        _id = util.save_csv(upload)
    except Exception:
        raise JsonError(description="Failed to create user. try again.")
    return json_response(id=_id)

@app.route("/set_name", methods=["POST"])
def save_user(username):
    data = request.get_json()
    user_id = get_user(data.get("id"))
    new_name = data.get("name")
    try:
        util.set_username(user_id, new_name)
    except Exception:
        raise JsonError(description="Failed to set username.")
    return json_response(user=_user)


@app.route("/get_score", methods=["POST"])
def get_score():
    id = request.forms.get("id")
    _name, _score = util.get_your_data(id)
    return render_template("result.html", name=_name, score=_score)

@app.route("/ranking/yours", methods=["GET"])
def your_ranking():
    _name, _score = util.get_your_data(request.args.get("id",""))
    return render_template("ranking_with_your_score.html", name=_name, score=_score)

@app.route("/ranking")
def ranking():
    return render_template("ranking.html")

if __name__ == '__main__':
    app.run()
