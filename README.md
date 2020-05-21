# pygc

A library to interact with genesiscloud

## Demo

Initialize the client:
```
>>> from pygc.client import Client
>>> client = Client("yourapikey")
```

List available SSH keys:
```
>>> [i for i in client.SSHKeys.find({"name": 'oz123@genesiscloud.com'})]
[{'id': '650e5ecb-4e28-4a24-bfbf-ac4212f7e137',
  'name': 'oz123@genesiscloud.com',
  'public_key': 'ssh-rsa AAA...RJCcsdx',
  'created_at': '2020-03-17T14:46:21.443Z'}]
```

List all images which can be used to create an instance:
```

>>> [i for i in client.Images.find({"type": 'base-os'})]
[{'id': '45d06539-f8f5-48d9-816e-d4b1a8e5163e',
  'name': 'Ubuntu 18.04',
  'type': 'base-os',
  'created_at': '2020-03-24T18:14:01.223Z'},
 {'id': '6d5c3613-f6cb-48e1-8711-14f084060209',
  'name': 'Ubuntu 16.04',
  'type': 'base-os',
  'created_at': '2020-03-24T18:14:01.219Z'}]
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
## Contributing to this project

First, make sure you have pipenv installed.

Run `pipenv shell` and then `pipenv install`.

Write your tests, add your features, test your features with `make test`.
`git commit` and `git push` :-)

Make a PR!
