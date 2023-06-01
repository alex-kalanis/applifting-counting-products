#######################
# Main flask app file #
#######################

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .environment import uri_path

# creating the flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri_path()

db = SQLAlchemy(app)
migrate = Migrate(app, db)
