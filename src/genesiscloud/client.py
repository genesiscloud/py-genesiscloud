# MIT License
#
# Copyright (c) 2020 Genesis Cloud Ltd. <opensource@genesiscloud.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Authors:
#   Oz Tiram <otiram@genesiscloud.com>

import os
import sys

import requests

from munch import Munch


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"{self.message}"


GENESISCLOUD_API_ROOT = os.environ.get("GENESISCLOUD_API_ROOT",
                                       "https://api.genesiscloud.com/")


RESOURCES = {'Images': 'images',
             'Instances': 'instances',
             'SSHKeys': 'ssh-keys',
             'SecurityGroups': 'security-groups',
             'Snapshots': 'snapshots'}


INSTANCE_TYPES = {
    'vcpu-4_memory-12g_disk-80g_nvidia1080ti-1':
    {"vCPUs": 4, "RAM":  12, "Disk": 80, "GPU": 1},
    'vcpu-8_memory-24g_disk-80g_nvidia1080ti-2':
    {"vCPUs": 8, "RAM":  24, "Disk": 80, "GPU": 2},
    'vcpu-12_memory-36g_disk-80g_nvidia1080ti-3':
    {"vCPUs": 12, "RAM": 36, "Disk": 80, "GPU": 3},
    'vcpu-16_memory-48g_disk-80g_nvidia1080ti-4':
    {"vCPUs": 16, "RAM": 48, "Disk": 80, "GPU": 4},
    'vcpu-20_memory-60g_disk-80g_nvidia1080ti-5':
    {"vCPUs": 20, "RAM": 60, "Disk": 80, "GPU": 5},
    'vcpu-24_memory-72g_disk-80g_nvidia1080ti-6':
    {"vCPUs": 24, "RAM": 72, "Disk": 80, "GPU": 6},
    'vcpu-28_memory-84g_disk-80g_nvidia1080ti-7':
    {"vCPUs": 28, "RAM": 84, "Disk": 80, "GPU": 7},
    'vcpu-32_memory-96g_disk-80g_nvidia1080ti-8':
    {"vCPUs": 32, "RAM": 96, "Disk": 80, "GPU": 8},
    'vcpu-36_memory-108g_disk-80g_nvidia1080ti-9':
    {"vCPUs": 36, "RAM": 108, "Disk": 80, "GPU": 9},
    'vcpu-40_memory-120g_disk-80g_nvidia1080ti-10':
    {"vCPUs": 40, "RAM": 120, "Disk": 80, "GPU": 10},
}


class GenesisResource:
    """
    Template class to represent an API end point
    """
    def __init__(self, apikey):
        self.base_url = GENESISCLOUD_API_ROOT
        self.apikey = apikey

    @property
    def headers(self):
        return {"Content-Type": "application/json", "X-Auth-Token": self.apikey}

    def munchify(self, item):
        return getattr(sys.modules[__name__],
                       self.__class__.__name__[:-1])(item)

    def __list(self, page=1, items=10, json=False, raw=False, **kwargs):  # noqa
        response = requests.get(
            self.base_url + f"compute/v1/{self._route}",
            headers=self.headers,
            params={"page": page, "per_page": items}
        )
        if response.status_code != 200:
            raise APIError(response.status_code, response.content)

        if json:
            yield response.json()['instances']
        if raw:
            yield response.json()
        else:
            for item in response.json()[self._route.replace("-", "_")]:
                yield self.munchify(item)

    def get(self, id):
        response = requests.get(
            self.base_url + f"compute/v1/{self._route}/{id}",
            headers=self.headers)

        if response.status_code != 200:
            raise APIError(response.status_code, response.content)

        return self.munchify(response.json()[f"{self._route[:-1]}"])

    def list(self, page=1, items=10, json=False, raw=False):  # noqa

        if json:
            return next(self.__list(page=page, items=items, json=True))
        if raw:
            return next(self.__list(page=page, items=items, raw=True))
        else:
            return self.__list(page=page, items=items)

    def find(self, filter):

        page = 1
        try:
            for item in self.list(page=page, items=100):
                for key, value in filter.items():
                    if key in item and item[key] == value:
                        yield self.munchify(item)
            page += 1
        except APIError:
            return {}

    def create(self, **kwargs):
        response = requests.post(
            self.base_url + f"compute/v1/{self._route}",
            headers=self.headers,
            json=kwargs
        )
        if response.status_code != 201:
            raise APIError(response.status_code, response.content)

        return self.munchify(response.json()[f"{self._route[:-1]}"])

    def delete(self, id, **kwargs):
        response = requests.delete(
            self.base_url + f"compute/v1/{self._route}/{id}",
            headers=self.headers,
        )
        if response.status_code != 204:
            raise APIError(response.status_code, response.content)


class ItemView(Munch):
    """
    Template class to represent an item returned from the API
    """
    api_to_resouce = {'ssh_keys': 'SSHKey',
                      'security_groups': 'SecurityGroup'}

    def __getattr__(self, k):
        v = super().__getattr__(k)
        if isinstance(v, (dict, Munch)):
            return getattr(sys.modules[__name__], k.capitalize())(v)
        if isinstance(v, list):
            kls = getattr(sys.modules[__name__],
                          ItemView.api_to_resouce[k])
            return [kls(i) for i in v]
        return v


for resource, route in RESOURCES.items():
    locals()[resource] = type(resource,
                              (GenesisResource, object),
                              {"_route": route})

    single_item = resource[:-1]
    locals()[single_item] = type(single_item,
                                 (ItemView, object),
                                 {})


def create_snapshot(obj, **kwargs):
    response = requests.post(
        obj.base_url + "compute/v1/instances/%s/snapshots" % kwargs.pop('instance_id'),  # noqa
        headers=obj.headers,
        json=kwargs
    )
    if response.status_code != 201:
        raise APIError(response.status_code, response.content)

    return obj.munchify(response.json()[f"{obj._route[:-1]}"])


setattr(getattr(sys.modules[__name__], "Snapshots"), "create", create_snapshot)


class Client:

    def __init__(self, apikey):
        self.apikey = apikey
        self.base_url = GENESISCLOUD_API_ROOT

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
