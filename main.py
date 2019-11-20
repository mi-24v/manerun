from flask import Flask, request, render_template, redirect, url_for, abort
from flask_json import FlaskJSON, JsonError, jsonify,json_response, as_json

import util

app = Flask(__name__)


"""
    Top page redirects to ranking page.
"""
@app.route("/")
def index():
    return redirect(url_for('ranking'))

"""
    Receive motion data.
    This request must contain one 'motion format' csv file.
    This may need authorization.
"""
@app.route('/upload', methods=['POST'])
def do_upload():
    upload = request.files['upload']
    if not upload.filename.lower().endswith(('.csv')):#TODO verfy RIGHT WAY
        raise JsonError(description="Invalid file.")
    try:
        _id = util.save_csv(upload)
    except Exception:
        raise JsonError(description="Failed to create user. try again.")
    return jsonify(id=_id)

"""
    Display form which associates with id and displayed name.
    This need authorization.

    request params
        `id_number` : id such as `'d8a272d9-be39-4d81-96dc-78626ac1b5d3'`
    return
        a form of registration.
"""
@app.route("/regist/<id_number>")
def do_regist(id_number):
    return render_template("regist.html",id_number=id_number)

"""
    Associates with display name and id.
    This needs authorization.

    request params
        id : id such as `'d8a272d9-be39-4d81-96dc-78626ac1b5d3'`
        name : name that you want to set like "John"
    returns
        A JSON.
        If it success, which contains name, else error description.
"""
@app.route("/set_name", methods=["POST"])
def save_user():
    data = request.get_data()
    print(data)
    print(request.form["name"])
    print(request.form["id"])
    return(request.form["name"])
    user_id = get_user(request.form["id"])
    new_name = request.form["name"]
    try:
        util.set_username(user_id, new_name)
    except Exception:
        raise JsonError(description="Failed to set username.")
    return json_response(user=_user)

"""
    Ask DB for user information such as score.
    This needs authorization.

    request params
        id : which id you want to ask. such as `'d8a272d9-be39-4d81-96dc-78626ac1b5d3'`
    returns
        A page which contains user's score data.
"""
@app.route("/get_score", methods=["POST"])
def get_score():
    id = request.forms.get("id")
    _name, _score = util.get_your_data(id)
    return render_template("result.html", name=_name, score=_score)

"""
    Display score ranking.
    This needs authorization.

    request params
        id : which id you want to ask. such as `'d8a272d9-be39-4d81-96dc-78626ac1b5d3'`
    returns
        A page which contains users' ranking.
"""
@app.route("/ranking/yours", methods=["GET"])
def your_ranking():
    _name, _score = util.get_your_data(request.args.get("id",""))
    return render_template("ranking_with_your_score.html", name=_name, score=_score)

"""
    Display score ranking.
    This **doesn't** need authorization.

    returns
        A page which contains users' ranking.
"""
@app.route("/ranking")
def ranking():
    db = {"unchi":90,"OMMC":65,"ゆゆうた":70,"KMR":85}
    ranking_data = sorted(db.items(), key=lambda x:x[1])
    return render_template("ranking.html",ranking_data = ranking_data)


if __name__ == '__main__':
    #app.run() #TODO comment out on deploy
    app.run(host='192.168.3.128', port=8000) #TODO remove on deploy
