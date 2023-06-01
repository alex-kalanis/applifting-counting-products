from flask import jsonify
from flask_httpauth import HTTPTokenAuth
from .repository import UserRepository
from .confs import ConfigAdmin

# @link https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis

# ************************************** #
#  Authenticate user to access products  #
# ************************************** #
token_auth_products = HTTPTokenAuth()


@token_auth_products.verify_token
def verify_token(token):
    return UserRepository().is_token(token) if token else None


@token_auth_products.error_handler
def token_auth_error(status):
    res = jsonify({'error': status})
    res.status = 401
    return res


# ************************************************ #
#  Authenticate master user to access other users  #
# ************************************************ #
token_auth_system = HTTPTokenAuth()


@token_auth_system.verify_token
def verify_token(token):
    return (ConfigAdmin.static().get() == token) if token else None


@token_auth_system.error_handler
def token_auth_error(status):
    res = jsonify({'error': status})
    res.status = 401
    return res
