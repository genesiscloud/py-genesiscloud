# pygc

A library to interact with genesiscloud

## Demo

```
>>> from pygc.client import Client
>>> client = Client("yourapikey")
# list available SSH keys
>>> [i for i in client.SSHKeys.find({"name": 'oz123@genesiscloud.com'})]
[{'id': '650e5ecb-4e28-4a24-bfbf-ac4212f7e137',
  'name': 'oz123@genesiscloud.com',
  'public_key': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDEXGmK8mZQtr1jFk/Sznuy75YBBRETYVgT01iqQ9wIWKTkt2ocYXHsiYWN9FlwDcnx49i1+jiocxtLOoXMvhH7BZc1sH9x1ty+w23feHVcmYe6AkmhjTlFUcnkjyKEaGRK5NpvGbIXuX/GrvARBr98xex23qV7dBzJnFrQ0vZkez8ryB+rOsI49q+OtSM3LtdMGwsxeiYg2t0YAyPJQ/vC97FyS+0oXs2wcl9wAnj1TRCWXT1zuhRk0xqzHtVtFwqAM13q4GWVmSSOT9+sMEo+7uS/ybxjT5y0IfqteLzxgVOA73P3qDOPxzg7I+O1f1wBnisE3KJMrh3BdRJCcsdx',
  'created_at': '2020-03-17T14:46:21.443Z'}]
# list all images which can be used to create an instance
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


## Contributing to this project

First, make sure you have pipenv installed.

Run `pipenv shell` and then `pipenv install`.

Write your tests, add your features, test your features with `make test`.
`git commit` and `git push` :-)

Make a PR!
