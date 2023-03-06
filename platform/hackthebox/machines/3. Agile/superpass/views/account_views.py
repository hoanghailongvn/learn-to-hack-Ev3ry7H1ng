import flask
import string
from flask_login import login_user, logout_user
from superpass.infrastructure.view_modifiers import response
from superpass.services import user_service

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    return {}


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    r = flask.request
    username = r.form.get('username', '').strip()
    password = r.form.get('password', '').strip()

    if not username or not password:
        return {
            'error': 'Please fill in username and password',
            'username': username
        }

    if len([c for c in username if c not in string.ascii_letters + string.digits]) > 0:
        return {
            'error': 'Please use only letters and numbers in usernames',
            'username': username,
        }

    user = user_service.create_user(username, password)
    if not user:
        return {
            'error': 'User already exists',
            'username': username,
        }

    login_user(user, remember=True)
    return flask.redirect('/vault')


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return{}


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():
    
    r = flask.request
    username = r.form.get('username', '').strip()
    password = r.form.get('password', '').strip()

    if not username or not password:
        return {
            'error': 'Please fill in username and password',
            'username': username
        }

    user = user_service.login_user(username, password)

    if not user:
        return {
            'error': 'Login failed',
            'username': username,
        }

    login_user(user, remember=True)
    return flask.redirect(flask.url_for('vault.vault'))


@blueprint.route('/account/logout')
def logout():
    logout_user()
    return flask.redirect(flask.url_for('home.index'))

