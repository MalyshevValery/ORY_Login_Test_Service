"""Main code of the app"""
import json
from typing import Optional

import requests
from flask import Flask, render_template, Response, request
from flask_material import Material
from werkzeug.utils import secure_filename

from config import LOGIN_TYPES, URL
from secrets import SECRETS

app = Flask(__name__)
Material(app)


@app.route('/static/<path>', methods=['GET'])
def get_file(path: str):
    """Returns static files"""
    secured = secure_filename(path)
    return Response(open('static/' + secured))


def check_login() -> Optional[str]:
    """Check if user is logged in"""
    return None


@app.route('/', methods=['GET'])
def page():
    """Returns main page with login button(s) and login check"""
    info = check_login()
    if info is None:
        info = 'Anonymous ! ! !'
    logins = list(LOGIN_TYPES.items())
    return render_template('main.html', name=info, logins=logins)


@app.route('/login/<login_type>', methods=['GET'])
def login(login_type: str):
    """Redirect to login screen (not yet implemented)"""
    base_link = LOGIN_TYPES[login_type]
    config = SECRETS[login_type]
    link = f'{base_link}?client_id={config.id}'
    link += f'&response_type=code&redirect_uri={URL}/profile/{login_type}'
    if config.scope is not None:
        link += f'&scope={config.scope}'
    return render_template('login.html', login_type=login_type,
                           login_link=link)


@app.route('/profile/<login_type>', methods=['GET'])
def profile(login_type: str):
    """Profile page of a user"""
    code = request.args.get('code')
    secret = SECRETS[login_type]
    print(f'{URL}/profile/{login_type}')
    r = requests.post(secret.access_url, data={
        'client_id': secret.id,
        'client_secret': secret.secret,
        'code': code,
        'redirect_uri': f'{URL}/profile/{login_type}',
        'grant_type': 'authorization_code',
    }, headers={'Accept': 'application/json'})
    res = json.loads(r.text)
    if 'error' in res:
        return render_template('error.html', error=res['error'])
    else:
        access_token = res['access_token']
        r = requests.get(secret.info_url, headers={
            'Authorization': secret.header % access_token,
            'Accept': 'application/json',
        })
        res = json.loads(r.text)
        print(res)
        return render_template('profile.html', type=login_type,
                               name=secret.get_name(res))


if __name__ == '__main__':
    app.run()
