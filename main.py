from flask import Flask, request, render_template, redirect, url_for, abort
from flask_json import FlaskJSON, JsonError, jsonify,json_response, as_json
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_firebaseauth import FirebaseAuth

import util
from model.user import User

import os

# app init
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['FIREBASE_API_KEY'] = os.environ.get("FIREBASE_API_KEY")
app.config['FIREBASE_PROJECT_ID'] = os.environ.get("FIREBASE_PROJECT_ID")
app.config['FIREBASE_AUTH_SIGN_IN_OPTIONS'] = "email,google"
# app login manager init
login_manager = LoginManager()
login_manager.init_app(app)
auth = FirebaseAuth(app)
app.register_blueprint(auth.blueprint, url_prefix='/auth')


"""
    Authorization.
"""

@app.route('/login/')
@login_required
def login():
    return redirect(url_for('ranking/yours'))

@app.route('/logout/')
def logout():
    return auth.sign_out()

@auth.unloader
def sign_out():
    logout_user()

@auth.production_loader
def production_loader(token, params):
    _id = util.check_contain_id(params, app.logger)
    user = util.get_user_with_token(_id ,token.get("user_id"))
    if user is not None:
        login_user(user, True)


@auth.development_loader
def development_loader(email):
    user = util.get_user(os.environ.get("DEBUG_USER_ID"))
    if user is not None:
        login_user(user, True)

@login_manager.user_loader
def user_loader(user_token):
    return util.get_user_from_token(user_token)

@login_manager.request_loader
def request_loader(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')
    id = request.args.get('id')
    return util.get_user_with_token(id, token)

@login_manager.unauthorized_handler
def authentication_required():
    _id = request.args.get('id')
    return redirect(auth.url_for('widget', mode='select', next=request.url, id=_id))


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
@app.route("/regist/<uuid:_id>")
@login_required
def do_regist(_id):
    return render_template("regist.html",id_number=_id)

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
@login_required
def save_user():
    new_name = request.form["name"]
    try:
        util.set_username(current_user.id, new_name)
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
@login_required
def get_score():
    user = util.get_your_data(current_user.id)
    _name = user.name
    _score = user.score
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
@login_required
def your_ranking():
    _score = util.get_your_data(current_user.id).score
    return render_template("ranking.html", userData = userData, scoreData = scoreData, score=_score)

"""
    Display score ranking.
    This **doesn't** need authorization.

    returns
        A page which contains users' ranking.
"""
@app.route("/ranking")
def ranking():
    userData, scoreData = util.get_ranking_data()
    return render_template("ranking.html", userData = userData, scoreData = scoreData)


if __name__ == '__main__':
    app.run() #TODO comment out on deploy
    # app.run(host='localhost', port=8000, debug=True) #TODO remove on deploy
