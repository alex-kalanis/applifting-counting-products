#######################
# Main flask app file #
#######################

from flask_restful import Api
from flask_swagger import swagger
from flask.cli import AppGroup
from swagger_ui import api_doc
from libs.environment import config
from libs.initial import create_app
import click

# creating an API object
app = create_app(None)
api = Api(app)

# adding the defined resources-controllers along with their corresponding urls
from libs.controllers import ProductController, OfferController, UserController
api.add_resource(ProductController, '/v1/product/')
api.add_resource(OfferController, '/v1/offer/')
api.add_resource(UserController, '/v1/user/')


# swagger with path
swag = swagger(app)
swag['info']['version'] = "1.0"
swag['info']['title'] = "Products counting api"
api_doc(app, config=swag, url_prefix='/v1/documentation', title='Counting api')

task_cli = AppGroup('tasks')


@task_cli.command("init")
@click.argument("master_key")
@click.argument("master_token")
def initial_run(master_key, master_token):
    from libs.confs import ConfigToken, ConfigAdmin

    ConfigAdmin.static().set(master_key)
    ConfigToken.static().set(master_token)


@task_cli.command("ping")
def ping_run():
    from libs.queues import ProductQueues

    ProductQueues.load_products_offer()


app.cli.add_command(task_cli)


@app.route('/')
def home():
    return 'Greetings to counting API; use documentation and readme to know more.'


# driver function
if __name__ == '__main__':

    app.run(
        host=config['APP_HOST'] if 'APP_HOST' in config else '0.0.0.0',
        port=config['APP_PORT'] if 'APP_PORT' in config else 80,
        debug=bool(config['DEBUG']) if 'DEBUG' in config else False
    )

