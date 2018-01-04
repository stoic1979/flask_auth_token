from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

from db import Mdb

app = Flask(__name__)

app.config['secretkey'] = 'some-strong+secret#key'

mdb = Mdb()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        # ensure that token is specified in the request
        if not token:
            return jsonify({'message': 'Missing token!'})

        # ensure that token is valid
        try:
            data = jwt.decode(token, app.config['secretkey'])
        except:
            return jsonify({'message': 'Invalid token!'})

        return f(data, *args, **kwargs)

    return decorated

@app.route('/unprotected')
def unprotected():

    return 'unprotected'

@app.route('/protected')
@token_required
def protected(data):
    # print "data: ", data
    return 'protected'




# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# NOT USING THIS AT THE MOMENT
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
@app.route('/login_old')
def login_old():
    auth = request.authorization

    if auth and auth.password == 'password':
        expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({'user': auth.username, 'exp': expiry}, app.config['secretkey'], algorithm='HS256')
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/login', methods=['POST'])
def login():

    ret = {'err': 0}
    try:

        email = request.form['email']
        password = request.form['password']

        if mdb.user_exists(email, password):

            # Login Successful!

            expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            token = jwt.encode({'user': email, 'exp': expiry}, app.config['secretkey'], algorithm='HS256')

            ret['msg'] = 'Login successful'
            ret['err'] = 0
            ret['token'] = token.decode('UTF-8')

        else:

            # Login Failed!

            ret['msg'] = 'Login Failed'
            ret['err'] = 1

    except Exception as exp:
        ret['msg'] = '%s' % exp
        ret['err'] = 1

    return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=True)
