from libs.environment import connect

connect()

from libs.models import User, Product


def test_new_user():
    user = User()
    user.name = 'someone'
    user.token = 'b3df4nb531sg35'
    assert user.name == 'someone'
    assert user.token == 'b3df4nb531sg35'
    assert user.deleted is None


def test_new_product():
    user = Product()
    user.uuid = 'dgh2sd4g23sd4g5'
    user.name = 'someone'
    user.desc = 'b3df4nb531sg35'
    assert user.uuid == 'dgh2sd4g23sd4g5'
    assert user.name == 'someone'
    assert user.desc == 'b3df4nb531sg35'
    assert user.deleted is None
