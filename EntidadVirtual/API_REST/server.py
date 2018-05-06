# /server.py

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
import requests
from functools import wraps
app = Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='KbPC5q-VuaUwBrkEP9_DY2-gWj-5t-Kt',
    client_secret='hM_dr9PBWS8fQ9Ijyd3veM-8lmJ43SF8BKFkFwuWu9ArKpnlle8197m4ajopCtY6',
    api_base_url='https://isis2503-softsecurity.auth0.com',
    access_token_url='https://isis2503-softsecurity.auth0.com/oauth/token',
    authorize_url='https://isis2503-softsecurity.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)


# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    resp = auth0.authorize_access_token()

    url = 'https://isis2503-softsecurity.auth0.com/userinfo'
    headers = {'authorization': 'Bearer ' + resp['access_token']}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()

    # Store the tue user information in flask session.
    session['jwt_payload'] = userinfo

    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect('/dashboard')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='file:///C:/Users/JuanCamilo/Music/201810_01_softsecurity/EntidadVirtual/API_REST/template/home.html', audience='https://isis2503-softsecurity.auth0.com/userinfo')

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'KbPC5q-VuaUwBrkEP9_DY2-gWj-5t-Kt'}
    return redirect(auth0.base_url + '/v2/logout?' + urlencode(params))

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)

    return decorated

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))