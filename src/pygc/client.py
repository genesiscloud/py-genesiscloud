import requests


class Client:

    def __init__(self, apikey):
        self.apikey = apikey
        self.base_url = "http://api.genesiscloud.com/"

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

    def _instances(self, page=1, items=10, json=False, raw=False):
        response = requests.get(self.base_url + "compute/v1/instances",
                                headers=self.headers,
                                params={"page": page, "per_page": items}
                                )
        if json:
            yield response.json()['instances']
        if raw:
            yield response.json()
        else:
            # TODO: create instance of gc.Instance for each item
            for item in response.json()['instances']:
                yield item

    def instances(self, page=1, items=10, json=False, raw=False):
        """
        List instances

        Keywords:
            page (int): page number
            items (int): items per page
            json (bool): return json response
            raw (bool): return raw json response
        """
        if json:
            return next(self._instances(page=page, items=items, json=True))
        if raw:
            return next(self._instances(page=page, items=items, raw=True))
        else:
            return self._instances(page=page, items=items)
