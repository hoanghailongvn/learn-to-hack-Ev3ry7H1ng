import json
import os
import sys
import flask
import jinja_partials
from flask_login import LoginManager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from superpass.infrastructure.view_modifiers import response
from superpass.data import db_session

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'MNOHFl8C4WLc3DQTToeeg8ZT7WpADVhqHHXJ50bPZY6ybYKEr76jNvDfsWD'


def register_blueprints():
    from superpass.views import home_views
    from superpass.views import vault_views
    from superpass.views import account_views
    
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(vault_views.blueprint)
    app.register_blueprint(account_views.blueprint)


def setup_db():
    db_session.global_init(app.config['SQL_URI'])


def configure_login_manager():
    login_manager = LoginManager()
    login_manager.login_view = 'account.login_get'
    login_manager.init_app(app)

    from superpass.data.user import User

    @login_manager.user_loader
    def load_user(user_id):
        from superpass.services.user_service import get_user_by_id
        return get_user_by_id(user_id)


def configure_template_options():
    jinja_partials.register_extensions(app)
    helpers = {
        'len': len,
        'str': str,
        'type': type,
    }
    app.jinja_env.globals.update(**helpers)


def load_config():
    config_path = os.getenv("CONFIG_PATH")
    with open(config_path, 'r') as f:
        for k, v in json.load(f).items():
            app.config[k] = v


def configure():
    load_config()
    register_blueprints()
    configure_login_manager()
    setup_db()
    configure_template_options()


def enable_debug():
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
    app.debug = True


def main():
    enable_debug()
    configure()
    app.run(debug=True)


def dev():
    configure()
    app.run(port=5555)


if __name__ == '__main__':
    main()
else:
    configure()
