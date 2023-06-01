from .db import Db
from .models import Config, Product, ProductOffer, User
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


class ProductRepository:

    def add(self, uuid: str, name: str, desc: str) -> bool:
        product = Product()
        product.uuid = uuid
        product.name = name
        product.desc = desc
        product.deleted = None

        db = Db.static().get_session()
        db.add(product)
        db.commit()
        return True

    def read(self, uuid: str, also_deleted: bool = False) -> Product or None:
        db = Db.static().get_session()
        q = db.query(Product)
        q.filter(Product.uuid==uuid)
        if not also_deleted:
            q.filter(Product.deleted==None)
        q.order_by(ProductOffer.added.desc())
        return q.first()

    def update(self, uuid: str, name: str, desc: str) -> bool:
        product = self.read(uuid, True)
        if not product:
            # not exists - add
            return self.add(uuid, name, desc)

        db = Db.static().get_session()
        product.name = name if name else product.name
        product.desc = desc if desc else product.desc
        if product.deleted is not None:
            product.deleted = None
        db.commit()
        return True

    def delete(self, uuid: str) -> bool:
        db = Db.static().get_session()
        product = self.read(uuid, True)
        if not product:
            return True
        if product.deleted is None:
            product.deleted = datetime.now()
        else:
            db.delete(product)
        db.commit()
        return True

    def all_available(self, also_deleted: bool = False):
        """
        Get all available products

        Parameters
        ----------
        also_deleted : bool, default=False

        Return
        ----------
        list[Product]
        """
        db = Db.static().get_session()
        q = db.query(Product)
        if not also_deleted:
            q.filter(Product.deleted==None)
        q.order_by(ProductOffer.added.desc())
        return q.all()


class OfferRepository:

    def add(self, product_id: int, price: int, pieces: int) -> bool:
        db = Db.static().get_session()

        offer = ProductOffer()
        offer.product_id = product_id
        offer.price = price
        offer.pieces = pieces

        db.add(offer)
        db.commit()
        return True

    def latest(self, product_id: int) -> ProductOffer or None:
        db = Db.static().get_session()
        q = db.query(ProductOffer)\
            .filter(ProductOffer.product_id==product_id)\
            .order_by(ProductOffer.added.desc())
        return q.first()

    def delete(self, pk: int) -> bool:
        db = Db.static().get_session()
        to_delete = db.query(ProductOffer).filter(ProductOffer.id==pk).first()
        db.delete(to_delete)
        db.commit()
        return True


class UserRepository:

    def add(self, name: str, token: str) -> bool:
        db = Db.static().get_session()

        usr = User()
        usr.name = name
        usr.token = token
        usr.deleted = None

        db.add(usr)
        db.commit()
        return True

    def read(self, name: str, also_deleted: bool = False) -> User or None:
        db = Db.static().get_session()
        q = db.query(User)
        if not also_deleted:
            q.filter(Product.deleted==None)
        q.filter(User.name==name)
        return q.first()

    def is_token(self, token: str) -> bool:
        db = Db.static().get_session()
        q = db.query(User)
        q.filter(User.deleted==None)
        q.filter(User.token==token)
        try:
            q.first()
            return True
        except SQLAlchemyError:
            return False

    def update(self, name: str, token: str) -> bool:
        usr = self.read(name, True)
        if not usr:
            # not exists - add
            return self.add(name, token)

        db = Db.static().get_session()
        usr.token = token if token else usr.token
        if usr.deleted is not None:
            usr.deleted = None
        db.commit()
        return True

    def delete(self, name: str) -> bool:
        db = Db.static().get_session()
        usr = self.read(name, True)
        if not usr:
            return True
        if usr.deleted is None:
            usr.deleted = datetime.now()
        else:
            db.delete(usr)
        db.commit()
        return True


class ConfigRepository:

    def add(self, key: str, value) -> bool:
        db = Db.static().get_session()

        conf = Config()
        conf.key = key
        conf.value = value

        db.add(conf)
        db.commit()
        return True

    def read(self, key: str) -> Config or None:
        db = Db.static().get_session()
        return db.query(Config)\
            .filter(Config.key==key)\
            .first()

    def read_all(self):
        db = Db.static().get_session()
        return db.query(Config).all()

    def update(self, key: str, value) -> bool:
        db = Db.static().get_session()
        result = db.query(Config).filter(Config.key == key).first()
        result.value = value
        db.commit()
        return True

    def delete(self, key: str) -> bool:
        db = Db.static().get_session()
        to_delete = db.query(Config).filter(Config.key == key).first()
        db.delete(to_delete)
        db.commit()
        return True
