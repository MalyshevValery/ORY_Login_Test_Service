"""Main code of the app"""
from typing import Optional

from flask import Flask, render_template, Response
from flask_material import Material
from werkzeug.utils import secure_filename

from config import LOGIN_TYPES

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


if __name__ == '__main__':
    app.run()
