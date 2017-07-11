from pymongo import MongoClient
from config import *
from flask import jsonify
import traceback

import json
from bson import ObjectId


###########################################
# _id of mongodb record was not getting   #
# JSON encoded, so using this custom one  #
###########################################
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class Mdb:

    def __init__(self):
        conn_str = "mongodb://%s:%s@%s:%d/%s" \
                   % (DB_USER, DB_PASS, DB_HOST, DB_PORT, AUTH_DB_NAME)
        client = MongoClient(conn_str)
        self.db = client[DB_NAME]

    def add_user(self, user, email, password):
        try:
            rec = {
                'user': user,
                'email': email,
                'password': password
            }
            self.db.user.insert(rec)
        except Exception as exp:
            print "login() :: Got exception: %s", exp
            print(traceback.format_exc())


if __name__ == "__main__":
    mdb = Mdb()

    # quick internal tests
    mdb.add_user('johny', 'johny@gmail.com', '123')
    # lets write some users
    print "user created"

    # lets show all users
    for user in mdb.db.user.find():
        print "User: ", user
