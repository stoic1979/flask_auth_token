from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['secretkey'] = 'some-strong+secret#key'

@app.route('/unprotected')
def unprotected():
    return 'unprotected'

@app.route('/protected')
def protected():
    return 'protected'


@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({'user': user.username, 'exp': expiry})
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
