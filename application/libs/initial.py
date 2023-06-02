#######################
# Main flask app file #
#######################

import os
from flask import Flask
from .environment import uri_path, connect


def create_app(test_config):
    # creating the flask app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is str:
        app.config.from_pyfile(test_config)
    elif test_config is dict:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = uri_path()

    # connect DB
    connect()
    from .models import init_db_app
    init_db_app(app)

    return app
