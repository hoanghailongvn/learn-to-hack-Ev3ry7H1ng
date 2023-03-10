import flask
from superpass.infrastructure.view_modifiers import response

blueprint = flask.Blueprint('home', __name__, template_folder='templates')

@blueprint.route('/')
@response(template_file='home/index.html')
def index():
    return {}