from flask import jsonify, request
from flask.wrappers import Response
from flask_restful import Resource
from .auth import token_auth_products, token_auth_system
from .repository import ProductRepository, OfferRepository, UserRepository
from .exceptions import CountingException
from .queues import ProductQueues

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.


class ProductController(Resource):

    # Corresponds to GET request
    def get(self) -> Response:
        """
        Get stored product
        ---
        tags:
          - products
        parameters:
          - in: body
            name: body
            schema:
              id: Product
              required:
                - uuid
              properties:
                uuid:
                  type: string
                  description: uuid of product
                deleted:
                  type: int
                  description: if can be already soft-deleted
        responses:
          200:
            description: Product data
          404:
            description: Product not found
          400:
            description: Other error
        """
        try:
            data = request.get_json()
            if 'uuid' not in data:
                raise CountingException('You must set uuid!', 400)
            product = ProductRepository().read(
                str(data['uuid']),
                'deleted' in data and bool(int(data['deleted']))
            )
            if not product:
                raise CountingException('Product not found!', 404)

            return jsonify({'data': {
                'uuid': product.uuid,
                'name': product.name,
                'desc': product.desc,
            }})
        except CountingException as ex:
            res = jsonify({'error': str(ex)})
            res.status = ex.get_code() if ex.get_code() else 400
            return res

    # Corresponds to PUT request
    @token_auth_products.login_required
    def put(self) -> Response:
        """
        Update info about product
        ---
        tags:
          - products
        parameters:
          - in: body
            name: body
            schema:
              id: Product
              required:
                - uuid
              properties:
                uuid:
                  type: string
                  description: uuid of product
                name:
                  type: string
                  description: name of product
                desc:
                  type: string
                  description: product decription
                deleted:
                  type: int
                  description: if can be already soft-deleted
        responses:
          200:
            description: Product hes been updated
          401:
            description: User not authorized
          404:
            description: Product not found
          419:
            description: Error with updating
          400:
            description: Other error
        """
        try:
            data = request.get_json()
            if 'uuid' not in data:
                raise CountingException('You must set uuid!', 400)
            repo = ProductRepository()
            product = repo.read(
                str(data['uuid']),
                'deleted' in data and bool(int(data['deleted']))
            )
            if not product:
                raise CountingException('Product not found!', 404)

            repo.update(
                product.uuid,
                str(data['name']) if 'name' in data else None,
                str(data['desc']) if 'desc' in data else None,
            )
            return jsonify({'data': 'OK'})
        except CountingException as ex:
            res = jsonify({'error': str(ex)})
            res.status = ex.get_code() if ex.get_code() else 400
            return res

    # Corresponds to POST request
    @token_auth_products.login_required
    def post(self) -> Response:
        """
        Add product to scrapper
        ---
        tags:
          - products
        parameters:
          - in: body
            name: body
            schema:
              id: Product
              required:
                - uuid
                - name
                - desc
              properties:
                uuid:
                  type: string
                  description: uuid of product
                name:
                  type: string
                  description: name of product
                desc:
                  type: string
                  description: product decription
                deleted:
                  type: int
                  description: if can be already soft-deleted
        responses:
          200:
            description: Product added
          401:
            description: User not authorized
          403:
            description: Product already exists
          400:
            description: Other error
        """
        try:
            data = request.get_json()
            if 'uuid' not in data:
                raise CountingException('You must set uuid!', 400)
            if 'name' not in data:
                raise CountingException('You must set name!', 400)
            repo = ProductRepository()
            product = repo.read(
                str(data['uuid']),
                'deleted' in data and bool(int(data['deleted']))
            )
            if product:
                raise CountingException('Product already found!', 403)

            repo.update(
                str(data['uuid']),
                str(data['name']),
                str(data['desc']) if 'desc' in data else None,
            )
            ProductQueues.add_product(str(data['uuid']), str(data['name']), str(data['desc']) if 'desc' in data else '')
            return jsonify({'data': 'OK'})
        except CountingException as ex:
            res = jsonify({'error': str(ex)})
            res.status = ex.get_code() if ex.get_code() else 400
            return res

    # Corresponds to DELETE request
    @token_auth_products.login_required
    def delete(self) -> Response:
        """
        Delete product

        First call is soft, second call is hard
        ---
        tags:
          - products
        parameters:
          - in: body
            name: body
            schema:
              id: Product
              required:
                - uuid
              properties:
                uuid:
                  type: string
                  description: local product UUID
        responses:
          200:
            description: Product deleted
          401:
            description: User not authorized
          404:
            description: Product not found
          400:
            description: Other error
        """
        try:
            data = request.get_json()
            if 'uuid' not in data:
                raise CountingException('You must set uuid!', 400)
            repo = ProductRepository()
            repo.delete(
                str(data['uuid'])
            )

            return jsonify({'data': 'OK'})
        except CountingException as ex:
            res = jsonify({'error': str(ex)})
            res.status = ex.get_code() if ex.get_code() else 400
            return res


class OfferController(Resource):

    # Corresponds to GET request
    def get(self) -> Response:
        """
        Get stored product
        ---
        tags:
          - products
          - offers
        parameters:
          - in: body
            name: body
            schema:
              id: Offer
              required:
                - uuid
              properties:
                uuid:
                  type: string
                  description: uuid of product
        responses:
          200:
            description: Product data
          404:
            description: Product not found
          400:
            description: Other error
        """
        try:
            data = request.get_json()
            if 'uuid' not in data:
                raise CountingException('You must set uuid!', 400)
            product_repo = ProductRepository()
            offer_repo = OfferRepository()
            product = product_repo.read(
                str(data['uuid']),
                'deleted' in data and bool(int(data['deleted']))
            )
            if not product:
                raise CountingException('Product not found!', 404)

            offer = offer_repo.latest(product.id)
            if not offer:
                raise CountingException('Offers not found!', 400)

            return jsonify({'data': {
                'uuid': product.uuid,
                'price': offer.price,
                'pieces': offer.pieces,
            }})
        except CountingException as ex:
            res = jsonify({'error': str(ex)})
            res.status = ex.get_code() if ex.get_code() else 400
            return res


class UserController(Resource):

    # Corresponds to GET request
    @token_auth_system.login_required
    def get(self) -> Response:
        """
        Get stored user
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - uuid
              properties:
                name:
                  type: string
                  description: name of processed user
                deleted:
                  type: int
                  description: if can be already soft-deleted
        responses:
          200:
            description: User data
          401:
            description: User not authorized
          404:
            description: User not found
          400:
            description: Other error
        """
        try:
            data = request.get_json()
            if 'name' not in data:
                raise CountingException('You must set name!', 400)
            usr = UserRepository().read(
                str(data['name']),
                'deleted' in data and bool(int(data['deleted']))
            )
            if not usr:
                raise CountingException('User not found!', 404)

            return jsonify({'data': {
                'name': usr.name,
            }})
        except CountingException as ex:
            res = jsonify({'error': str(ex)})
            res.status = ex.get_code() if ex.get_code() else 400
            return res

    # Corresponds to PUT request
    @token_auth_system.login_required
    def put(self) -> Response:
        """
        Update info about product
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - name
              properties:
                name:
                  type: string
                  description: name of user
                token:
                  type: string
                  description: user's token
                deleted:
                  type: int
                  description: if can be already soft-deleted
        responses:
          200:
            description: User hes been updated
          401:
            description: User not authorized
          404:
            description: User not found
          419:
            description: Error with updating
          400:
            description: Other error
        """
        try:
            data = request.get_json()
            if 'name' not in data:
                raise CountingException('You must set name!', 400)
            repo = UserRepository()
            usr = repo.read(
                str(data['name']),
                'deleted' in data and bool(int(data['deleted']))
            )
            if not usr:
                raise CountingException('User not found!', 404)

            repo.update(
                usr.name,
                str(data['token']) if 'token' in data else None,
            )
            return jsonify({'data': 'OK'})
        except CountingException as ex:
            res = jsonify({'error': str(ex)})
            res.status = ex.get_code() if ex.get_code() else 400
            return res

    # Corresponds to POST request
    @token_auth_system.login_required
    def post(self) -> Response:
        """
        Add user to allow change products
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - name
                - token
              properties:
                name:
                  type: string
                  description: name of user
                token:
                  type: string
                  description: user's token
                deleted:
                  type: int
                  description: if can be already soft-deleted
        responses:
          200:
            description: User added
          401:
            description: User not authorized
          403:
            description: User already exists
          400:
            description: Other error
        """
        try:
            data = request.get_json()
            if 'name' not in data:
                raise CountingException('You must set name!', 400)
            if 'token' not in data:
                raise CountingException('You must set token!', 400)
            repo = UserRepository()
            usr = repo.read(
                str(data['name']),
                'deleted' in data and bool(int(data['deleted']))
            )
            if usr:
                raise CountingException('User already found!', 403)

            repo.update(
                str(data['name']),
                str(data['token'])
            )
            return jsonify({'data': 'OK'})
        except CountingException as ex:
            res = jsonify({'error': str(ex)})
            res.status = ex.get_code() if ex.get_code() else 400
            return res

    # Corresponds to DELETE request
    @token_auth_system.login_required
    def delete(self) -> Response:
        """
        Delete user

        First call is soft, second call is hard
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - uuid
              properties:
                uuid:
                  type: string
                  description: local product UUID
        responses:
          200:
            description: User deleted
          401:
            description: User not authorized
          404:
            description: User not found
          400:
            description: Other error
        """
        try:
            data = request.get_json()
            if 'name' not in data:
                raise CountingException('You must set name!', 400)
            repo = UserRepository()
            repo.delete(
                str(data['name'])
            )

            return jsonify({'data': 'OK'})
        except CountingException as ex:
            res = jsonify({'error': str(ex)})
            res.status = ex.get_code() if ex.get_code() else 400
            return res
