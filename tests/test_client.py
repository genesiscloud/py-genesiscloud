import responses

from pygc.client import Client


def test_client_init():

    assert hasattr(Client('q12313123dfsd'), "apikey")


@responses.activate
def test_client_connect():
    responses.add(
        responses.HEAD,
        'http://api.genesiscloud.com/compute/v1/instances?per_page=1&page=1',
        status=200)
    Client("foobars3kr3k3y").connect().status_code == 200
