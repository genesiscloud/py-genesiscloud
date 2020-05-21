import sys

import requests

RESOURCES = {'Images': 'images',
             'Instances': 'instances',
             'SSHKeys': 'ssh-keys',
             'SecurityGroups': 'security-groups',
             'Snapshots': 'snapshots'}


class GenesisResource:

    def __init__(self, apikey):
        self.base_url = "https://api.genesiscloud.com/"
        self.apikey = apikey

    @property
    def headers(self):
        return {"Content-Type": "application/json", "X-Auth-Token": self.apikey}

    def __list(self, page=1, items=10, json=False, raw=False, **kwargs):
        print(self.base_url + f"compute/v1/{self._route}")
        response = requests.get(
                self.base_url + f"compute/v1/{self._route}",
                headers=self.headers,
                params={"page": page, "per_page": items}
                )

        if json:
            yield response.json()['instances']
        if raw:
            yield response.json()
        else:
            # TODO: create instance of gc.Instance for each item
            for item in response.json()[self._route.replace("-", "_")]:
                yield item

    def list(self, page=1, items=10, json=False, raw=False):

        if json:
            return next(self.__list(page=page, items=items, json=True))
        if raw:
            return next(self.__list(page=page, items=items, raw=True))
        else:
            return self.__list(page=page, items=items)


for resource, route in RESOURCES.items():
    locals()[resource] = type(resource,
                              (GenesisResource, object),
                              {"_route": route})


class Client:

    def __init__(self, apikey):
        self.apikey = apikey
        self.base_url = "https://api.genesiscloud.com/"

    @property
    def headers(self):
        return {"Content-Type": "application/json", "X-Auth-Token": self.apikey}

    def connect(self):
        params = {"per_page": 1, "page": 1}
        r = requests.get(self.base_url + "compute/v1/instances",
                         headers=self.headers,
                         params=params
                         )
        if r.status_code in [401, 403]:
            raise ConnectionRefusedError(dict(status_code=r.status_code,
                                              body=r.content))

        return r

    def __getattr__(self, name):
        return getattr(sys.modules[__name__], name)(self.apikey)
