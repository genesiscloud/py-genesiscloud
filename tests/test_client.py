import responses
from munch import Munch

from pygc.client import Client


SSH_RESPONSE = {'ssh_keys': [{'id': '848a6631-486a-4992-8a40-5a9027415d02',
                              'name': 'oz123',
                              'public_key':
                              ('ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIj3+Q0uK0'
                                  'lVNqYrqUUFMBajoUtFcLPHES2Xk0x8BvlV'),
                              'created_at': '2020-05-21T17:39:10.621Z'},
                             {'id': '999a6631-486a-4882-8a40-5a9027415d03',
                              'name': 'master-foo',
                              'public_key':
                              ('ssh-ed25519 AAAAC4NzbC1laDI1NTE54BBBBIj3+Q0uK0'
                                  'lVNqYrqUUFMBajoUtFcLPHES2Xk0x8BvlV'),
                              'created_at': '2020-05-22T20:39:10.621Z'}],

                'total_count': 2,
                'page': 1,
                'per_page': 10}


def test_client_init():

    assert hasattr(Client('q12313123dfsd'), "apikey")


@responses.activate
def test_client_connect():
    responses.add(
        responses.GET,
        'https://api.genesiscloud.com/compute/v1/instances?per_page=1&page=1',
        status=200)
    assert Client("foobars3kr3k3y").connect().status_code == 200


def test_attributes():

    from pygc.client import SSHKey
    sshkey = SSHKey({"name": "oz123"})
    assert isinstance(sshkey, Munch)
    assert sshkey.name == "oz123"


@responses.activate
def test_client_find_returns_munch():
    responses.add(
        responses.GET,
        'https://api.genesiscloud.com/compute/v1/ssh-keys?per_page=100&page=1',
        json=SSH_RESPONSE,
        status=200)

    client = Client("foobars3kr3k3y")

    m = next(client.SSHKeys.find({"name": "oz123"}))
    assert isinstance(m, Munch)
    assert m.name == "oz123"


@responses.activate
def test_client_list_returns_munches():
    responses.add(
        responses.GET,
        'https://api.genesiscloud.com/compute/v1/ssh-keys?per_page=10&page=1',
        json=SSH_RESPONSE,
        status=200)

    client = Client("foobars3kr3k3y")

    sshkeys = [key for key in client.SSHKeys.list()]
    for key in sshkeys:
        assert isinstance(key, Munch)
