# py-genesiscloud

A library to interact with [genesiscloud][1]

## Demo

Initialize the client:
```
>>> from genesiscloud.client import Client
>>> client = Client("yourapikey")
```

List available SSH keys:
```
>>> [i for i in c.SSHKeys.find({"name":"oz123"})]
[SSHKey({'id': '848a6631-486a-4992-8a40-5a9027415d02', 'name': 'oz123', 'public_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIj3+Q0uK0lVNqYrqUUFMBajoUtFcLPHES2Xk0x8BvlV', 'created_at': '2020-05-21T17:39:10.621Z'})]
```

List all images which can be used to create an instance:
```
>>> [i for i in client.Images.find({"type": 'base-os'})]
[Image({'id': '45d06539-f8f5-48d9-816e-d4b1a8e5163e', 'name': 'Ubuntu 18.04', 'type': 'base-os', 'created_at': '2020-03-24T18:14:01.223Z'}),
 Image({'id': '6d5c3613-f6cb-48e1-8711-14f084060209', 'name': 'Ubuntu 16.04', 'type': 'base-os', 'created_at': '2020-03-24T18:14:01.219Z'})]
```

Create an instance
```
>>> client.Instances.create(name='test-oz', hostname='hostname',
                            sshkeys=['650e5ecb-4e28-4a24-bfbf-ac4212f7e137']
                            type='vcpu-4_memory-12g_disk-80g_nvidia1080ti-1',
                            "image"='45d06539-f8f5-48d9-816e-d4b1a8e5163e',
                            "metadata"={"startup_script":"#!/bin/bash\nsudo apt update && sudo apt install iperf3"}
                            )
```

Accessing attributes of an Instance:
```
>>> inst = [i for i in client.Instances.list()][0]

>>> inst.security_groups[0]
SecurityGroup({'id': '2472c0bb-1fa9-4dcc-a658-4268e78ad907', 'name': 'default'})

>>> inst.security_groups
[SecurityGroup({'id': '2472c0bb-1fa9-4dcc-a658-4268e78ad907', 'name': 'default'}),
 SecurityGroup({'id': 'd3040f01-3b12-4712-9e8e-8ecb1ae7ba04', 'name': 'standard'}),
 SecurityGroup({'id': '56370632-ceeb-4357-a5d3-f2c3acf9d69e', 'name': 'Folding@home'})]

>>> inst.ssh_keys
[SSHKey({'id': '848a6631-486a-4992-8a40-5a9027415d02', 'name': 'oz123')]

>>> inst.image
Image({'id': '3c5f9b6f-2f4b-4067-ba50-925be9e6afb1', 'name': 'Ubuntu 18.04'})
```

## Contributing to this project

First, make sure you have pipenv installed.

Run `pipenv shell` and then `pipenv install`.

Write your tests, add your features, test your features with `make test`.
`git commit` and `git push` :-)

Make a PR!

[1] https://www.genesiscloud.com/
