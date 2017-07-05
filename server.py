from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['secretkey'] = 'some-strong+secret#key'

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

        return f(*args, **kwargs)

    return decorated

@app.route('/unprotected')
def unprotected():
    return 'unprotected'

@app.route('/protected')
@token_required
def protected():
    return 'protected'


@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({'user': auth.username, 'exp': expiry}, app.config['secretkey'], algorithm='HS256')
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)
