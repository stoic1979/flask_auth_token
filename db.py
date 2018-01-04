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

    def user_exists(self, email, password):
        """
        function checks if a user with given email and password
        exists in database
        :param email: email of the user
        :param password: password of the user
        :return: True, if user exists,
                 False, otherwise
        """
        return self.db.user.find({'email': email, 'password': password}).count() > 0


if __name__ == "__main__":
    mdb = Mdb()

    ########################
    #                      #
    # Quick internal tests #
    #                      #
    ########################

    # lets write some users
<<<<<<< HEAD
    # mdb.add_user('johny', 'johny@gmail.com', '123')
=======
    mdb.add_user('johny', 'johny@gmail.com', '123')
>>>>>>> 96b9b279acfd4998703433beaf950a6892f8af16
    print "user created"

    # lets show all users
    for user in mdb.db.user.find():
        print "User: ", user

<<<<<<< HEAD
    if mdb.user_exists('johny@gmail.com', '123'):
=======
    if mdb.user_exists('johny@gmail.com', '1234'):
>>>>>>> 96b9b279acfd4998703433beaf950a6892f8af16
        print "User exists"
    else:
        print "User does not exists"

