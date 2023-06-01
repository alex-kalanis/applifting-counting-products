import requests
from requests.auth import AuthBase
from .exceptions import CountingException


class BearerAuth(AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class Remote:
    """
    Queries to remote service
    """

    TOKEN_ADDRESS = 'https://python.applifting.cz/api/v1/auth'
    PRODUCT_ADDRESS = 'https://python.applifting.cz/api/v1/products/register'
    OFFER_ADDRESS = 'https://python.applifting.cz/api/v1/products/{}/offers'

    @staticmethod
    def get_token(master: str) -> str:
        response = requests.get(Remote.TOKEN_ADDRESS, auth=BearerAuth(master))
        if 200 == response.status_code:
            return str(response.json()['access_token'])
        else:
            raise CountingException(response.content, response.status_code)

    @staticmethod
    def add_product(uuid: str, name: str, desc: str, auth: str) -> bool:
        response = requests.get(Remote.PRODUCT_ADDRESS.format(uuid), data={
            'id': uuid,
            'name': name,
            'description': desc,
        }, auth=BearerAuth(auth))
        if 200 == response.status_code:
            return True
        elif 409 == response.status_code:
            # already known - not need to hassle
            return True
        else:
            raise CountingException(response.content, response.status_code)

    @staticmethod
    def get_product_offer(uuid: str, auth: str) -> dict:
        response = requests.get(Remote.OFFER_ADDRESS.format(uuid), auth=BearerAuth(auth))
        if 200 == response.status_code:
            obtained = dict(response.json())
            return {
                'uuid': obtained['id'],
                'price': obtained['price'],
                'pieces': obtained['items_in_stock'],
            }
        else:
            raise CountingException(response.content, response.status_code)
