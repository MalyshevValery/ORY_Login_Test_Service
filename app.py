"""Main code of the app"""
from typing import Optional
import json
from flask import Flask, render_template, Response, request
import requests
from flask_material import Material
from werkzeug.utils import secure_filename

from config import LOGIN_TYPES
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
    return render_template('login.html', login_type=login_type,
                           login_link=LOGIN_TYPES[login_type])


@app.route('/profile/<login_type>', methods=['GET'])
def profile(login_type: str):
    """Profile page of a user"""
    code = request.args.get('code')
    secret = SECRETS[login_type]
    r = requests.post(secret.access_url, data={
        'client_id': secret.id,
        'client_secret': secret.secret,
        'code': code
    }, headers={'Accept': 'application/json'})
    res = json.loads(r.text)
    if 'error' in res:
        return render_template('error.html', error=res['error'])
    else:
        access_token = res['access_token']
        r = requests.get('https://api.github.com/user', headers={
            'Authorization': f'token {access_token}',
            'Accept': 'application/json',
        })
        res = json.loads(r.text)
        print(res)
        return render_template('profile.html', type=login_type,
                               name=res['login'])


if __name__ == '__main__':
    app.run()
