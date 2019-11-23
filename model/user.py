from flask_login import UserMixin
import namegenerator

class User(UserMixin):

    # @staticmethod
    def _create_default_name():
        return namegenerator.gen()

    def __init__(self, id, motion_id, user_token="", name=_create_default_name(), score=0):
        self.id = id
        self.user_token = user_token
        self.name = name
        self.score = score
        self.motion_id = motion_id

    @staticmethod
    def from_dict(source):
        user = User(source["id"], source["motion_id"])

        if "user_token" in source:
            user.user_token = source["user_token"]

        if "name" in source:
            user.name = source["name"]

        if "score" in source:
            user.score = source["score"]

        return user

    def to_dick(self):
        dest = {
            "id" : self.id,
            "motion_id" : self.motion_id,
        }

        if self.user_token:
            dest["user_token"] = self.user_token

        if self.name:
            dest["name"] = self.name

        if self.score:
            dest["score"] = self.score

        return dest

    def __repr__(self):
        return "User(id={}, motion_id={}, user_token={}, name={}, score={})".format(self.id, self.motion_id, self.user_token, self.name, self.score)
