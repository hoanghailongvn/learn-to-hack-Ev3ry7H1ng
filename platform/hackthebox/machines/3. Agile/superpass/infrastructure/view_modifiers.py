from functools import wraps

import flask
from flask_login import current_user
import werkzeug
import werkzeug.wrappers


def response(*, mimetype: str = None, template_file: str = None):
    def response_inner(f):
        #print(f"Wrapping in response {f.__name__}", flush=True)

        @wraps(f)
        def view_method(*args, **kwargs):
            response_val = f(*args, **kwargs)

            if isinstance(response_val, werkzeug.wrappers.Response):
                return response_val

            if isinstance(response_val, flask.Response):
                return response_val

            if isinstance(response_val, dict):
                model = dict(response_val)
            else:
                model = dict()

            model['current_user'] = current_user

            if template_file and not isinstance(response_val, dict):
                raise Exception(
                    f"Invalid return type {type(response_val)}, we expected a dict as the return value.")

            if template_file:
                response_val = flask.render_template(template_file, **response_val)

            resp = flask.make_response(response_val)
            resp.model = model
            if mimetype:
                resp.mimetype = mimetype

            return resp

        return view_method

    return response_inner