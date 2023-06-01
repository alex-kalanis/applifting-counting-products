from .db import Redis
from rq import Queue
from .confs import ConfigToken
from .exceptions import CountingException
from .remote import Remote
from .repository import ProductRepository, OfferRepository


class ProductInQueue:
    """
    Tasks to work inside the queues
    """

    @staticmethod
    def available_products():
        """
        Get all products for getting offers and put them into queue for processing
        """
        # data = Remote.get_product_offer(uuid, ConfigToken.static().get())
        token = Remote().get_token(ConfigToken.static().get())
        products = ProductRepository().all_available()
        for product in products:
            ProductQueues.read_offer(product.uuid, token)

    @staticmethod
    def add_product(uuid: str, name: str, desc: str):
        """
        Insert new product to offer rotation

        Parameters
        ----------
        uuid : string
        name : string
        desc : string
        """
        token = Remote().get_token(ConfigToken.static().get())
        Remote.add_product(uuid, name, desc, token)

    @staticmethod
    def offer_for_product(uuid: str, token: str):
        """
        Insert new offer for product

        Parameters
        ----------
        uuid : string
        token : string
        """
        try:
            data = Remote.get_product_offer(uuid, token)
            product = ProductRepository().read(uuid)
            offers = OfferRepository()
            offers.add(product.id, data['price'], data['pieces'])
        except CountingException as ex:
            if 404 != ex.get_code():
                raise ex

class Queues:
    """
    Queues in Redis
    @link https://kb.objectrocket.com/redis/create-a-simple-task-queue-with-flask-and-redis-1467
    @link http://louistiao.me/posts/walkthrough-deploying-a-flask-app-with-redis-queue-rq-workers-and-dashboard-using-kubernetes/
    """

    queue = None

    def connect(self):
        Queues.queue = Queue(connection=Redis.static().get_connection())

    def get_queue(self) -> Queue:
        if not Queues.queue:
            raise CountingException('No queue set!')
        return Queues.queue


class ProductQueues:

    instance = None

    @staticmethod
    def get_queuing():
        if not ProductQueues.instance:
            ProductQueues.instance = Queues()
            ProductQueues.instance.connect()
        return ProductQueues.instance

    @staticmethod
    def load_products_offer():
        """
        Load all available products and put them into queue to get offers
        """
        ProductQueues.get_queuing().get_queue().enqueue(ProductInQueue.available_products)

    @staticmethod
    def add_product(uuid: str, name: str, desc: str):
        """
        Put product into queue to get current offer

        Parameters
        ----------
        uuid : string
        name : string
        desc : string
        """
        ProductQueues.get_queuing().get_queue().enqueue(ProductInQueue.add_product, uuid, name, desc)

    @staticmethod
    def read_offer(uuid: str, token: str):
        """
        Put product into queue to get current offer

        Parameters
        ----------
        uuid : string
        token : string
        """
        ProductQueues.get_queuing().get_queue().enqueue(ProductInQueue.offer_for_product, uuid, token)
