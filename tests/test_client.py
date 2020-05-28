import responses
import pytest

from munch import Munch

from genesiscloud.client import Client, SSHKey


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


INSTANCE_CREATE = {
    'instance':
        {'id': '54ca3596-e7e5-423d-8a76-5636127f0d8f',
         'name': 'demo',
         'hostname': 'demo',
         'type': 'vcpu-4_memory-12g_disk-80g_nvidia1080ti-1',
         'allowed_actions': ['start', 'shutoff', 'reset'],
         'ssh_keys': [{'id': 'c5fe90f8-659f-4c46-aaf6-85b962fed461',
                       'name': 'oz123'}],
         'image': {'id': '8860f26e-1f80-49eb-bf4f-aed47c6d1a63',
                   'name': 'Ubuntu 18.04-2020-05'},
         'security_groups': [
             {'id': 'cf8dbf46-7a59-4d7d-87f2-5a7d07cd76d6',
              'name': 'standard'}],
            'status': 'enqueued',
            'private_ip': None,
            'public_ip': None,
            'created_at':
            '2020-05-28T19:04:03.802Z',
            'updated_at': None}}


@pytest.fixture
def client():
    return Client('q12313123dfsd')


@responses.activate
def test_client_connect(client):
    responses.add(
        responses.GET,
        'https://api.genesiscloud.com/compute/v1/instances?per_page=1&page=1',
        status=200)
    assert client.connect().status_code == 200


def test_attributes():

    from genesiscloud.client import SSHKey
    sshkey = SSHKey({"name": "oz123"})
    assert isinstance(sshkey, Munch)
    assert sshkey.name == "oz123"


@responses.activate
def test_client_find_returns_munch(client):
    responses.add(
        responses.GET,
        'https://api.genesiscloud.com/compute/v1/ssh-keys?per_page=100&page=1',
        json=SSH_RESPONSE,
        status=200)

    m = next(client.SSHKeys.find({"name": "oz123"}))
    assert isinstance(m, Munch)
    assert m.name == "oz123"


@responses.activate
def test_client_list_returns_munches(client):
    responses.add(
        responses.GET,
        'https://api.genesiscloud.com/compute/v1/ssh-keys?per_page=10&page=1',
        json=SSH_RESPONSE,
        status=200)

    sshkeys = [key for key in client.SSHKeys.list()]
    for key in sshkeys:
        assert isinstance(key, Munch)


@responses.activate
def test_create_instance(client):

    responses.add(
        responses.POST,
        'https://api.genesiscloud.com/compute/v1/instances',
        json=INSTANCE_CREATE,
        status=201)

    inst = client.Instances.create(
        name="demo",
        hostname="demo",
        ssh_keys=['c5fe90f8-659f-4c46-aaf6-85b962fed461'],
        image='8860f26e-1f80-49eb-bf4f-aed47c6d1a63',
        type='vcpu-4_memory-12g_disk-80g_nvidia1080ti-1',
        )

    assert inst.name == "demo"
    assert isinstance(inst.ssh_keys[0], SSHKey)


@responses.activate
def test_get_instance(client):
    instance_id = INSTANCE_CREATE['instance']['id']
    responses.add(
        responses.GET,
        f'https://api.genesiscloud.com/compute/v1/instances/{instance_id}',
        json=INSTANCE_CREATE,
        status=200)

    inst = client.Instances.get(instance_id)

    assert inst.name == "demo"
    assert isinstance(inst.ssh_keys[0], SSHKey)
