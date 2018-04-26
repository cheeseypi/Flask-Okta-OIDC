from os import environ
from functools import wraps

import requests
from flask import Flask, redirect, url_for, request, session, abort

app = Flask(__name__)

app.secret_key = 'thisisasecret'

def query_string_gen(url, **kwargs):
    rtr = url + '?'
    for key,val in kwargs.items():
        rtr = rtr + key + '=' + val + '&'
    return rtr.strip('&')

def verify_token(token):
    data = {'client_id': environ.get('CLIENT_ID'), 'client_secret': environ.get('CLIENT_SECRET'), 'token': token, 'token_type_hint': 'access_token'}
    resp = requests.post(environ.get('OKTA_BASE_URL') + "/oauth2/default/v1/introspect", data).json()
    if not resp.get('active'):
        return False
    # Additional verification here
    return True

@app.route('/')
def homepage():
    return '''
    <p>Hello, world!</p>
    <p><a href="/login">Log in</a></p>
    <p><a href="/loginreq">Log-in restricted information</a></p>
    '''

@app.route('/login')
def loginpage():
    return redirect(query_string_gen(environ.get('OKTA_BASE_URL') + "/oauth2/default/v1/authorize", client_id=environ.get('CLIENT_ID'), response_type='code', redirect_uri='http://localhost:5000/authn-callback', nonce='hjdzbfmgjuhdrg', state='allgoodinthehood', scope='openid'))

@app.route('/authn-callback')
def signin():
    code = request.args.get('code')
    state = request.args.get('state')
    if state != 'allgoodinthehood':
        raise Exception('State Mismatch: '+str(state)+'=/=allgoodinthehood')
    data = {'code': code, 'client_id': environ.get('CLIENT_ID'), 'client_secret': environ.get('CLIENT_SECRET'), 'grant_type': 'authorization_code', 'redirect_uri': 'http://localhost:5000/authn-callback'}
    resp = requests.post(environ.get('OKTA_BASE_URL') + "/oauth2/default/v1/token", data).json()
    token = resp.get('access_token')
    if not verify_token(token):
        raise Exception('Invalid Token')
    session['token'] = token
    return redirect(url_for('homepage'))

@app.route('/loginreq')
def secret():
    if not verify_token(session.get('token')):
        abort(401)
    return '''
    <h1>RESTRICTED INFO</h1>
    '''

app.run('0.0.0.0')
