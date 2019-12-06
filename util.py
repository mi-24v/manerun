from google.cloud import firestore, storage

from model.user import User
# import ml

import uuid
# import threading
import ast


db = firestore.Client()
storage_client = storage.Client()
USER_KIND = "user"
MOTION_BUCKET_NAME = "manerun-motions"

def check_contain_id(dict_str_with_id, logger):
    logger.info("dict_str->{}\ntype of dict_str->{}".format(dict_str_with_id,type(dict_str_with_id)))
    try:
        _id = ast.literal_eval(dict_str_with_id)["id"][0]
        assert isinstance(uuid.UUID(_id), uuid.UUID), "{} is not UUID-String.".format(_id)
    except (ValueError, AssertionError) as e:
        logger.warn("invalid string found : {}\nexception detail :\n{}".format(dict_str_with_id, e))
    logger.info("id->{}".format(_id))
    return _id

def get_user(id):
    user_ref = db.collection(USER_KIND).document(id).get()
    if user_ref.exists:
        user = User.from_dict(user_ref.to_dict())
    else:
        user = None
    return user

def get_user_from_token(user_token):
    user_list = list(db.collection(USER_KIND).where("user_token" , "==", user_token).stream())
    if len(user_list) is 1:
        return User.from_dict(user_list[0].to_dict())
    else:
        return None

def get_user_with_token(id, user_token):
    if id is None or user_token is None:
        return None
    user = get_user(id)
    if user.user_token == "":
        db.collection(USER_KIND).document(id).update({"user_token":user_token})
    return user

def create_user():
    id = str(uuid.uuid4())
    csv_id = str(uuid.uuid4())
    user = User(id, csv_id)
    db.collection(USER_KIND).document(user.id).set(user.to_dict())
    return id

def save_csv(csv):
    user = create_user()
    insert_csv(user.csv_id, csv)
    # threading.Thread(target=ml.delegate_ML, args=(user,)).start()
    return user.id

def set_user_name(id, name):
    db.collection(USER_KIND).document(id).update({"name":name})

def get_ranking_data():
    name_list = []
    score_list = []
    ranking_stream = db.collection(USER_KIND).select(["name","score"]).order_by("score", direction="DESCENDING").stream()
    for data in ranking_stream:
        name_list.append(data.get("name"))
        score_list.append(data.get("score"))

    rank = ["1st ","2nd ","3rd "]
    rank += [str(i+4)+"th " for i in range( len(score_list)-3)]
    userData = [rank[i] + name_list[i]+"\t" for i in range(len(name_list))]
    return name_list, score_list

def get_your_data(id):
    return User.from_dict(db.collection(USER_KIND).document(id).get().to_dict())

def insert_csv(file_name, file):
    bucket = storage_client.get_bucket(MOTION_BUCKET_NAME)
    blob = bucket.blob(file_name)
    blob.upload_from_string(file.read(),file.content_type)

