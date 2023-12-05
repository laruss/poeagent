import json
import logging

from typing import Dict

from cloudscraper import CloudScraper

from .exceptions import SessionException
from .js import JS
from .models import RequestParams, TchannelData
from .queries import Queries

logger = logging.getLogger(__name__)


class ApiSession(CloudScraper):
    base_url = "https://poe.com"

    settings_url = "/api/settings"
    gql_post_url = "/api/gql_POST"

    def __init__(self, token: str, cookies: dict = None, *args, **kwargs):
        cookies = cookies or {}
        cookies.update({"p-b": token})

        super().__init__(*args, **kwargs)

        [self.cookies.set(name, value) for name, value in cookies.items()]

        self.js: JS = None
        self.requests_params: Dict[str, RequestParams] = None
        self.form_key: str = None
        self.tchannel_data: TchannelData = None

        self.__init_data_from_scripts()

    def __init_data_from_scripts(self):
        self.js = JS(self.get("/").text)
        self.form_key = self.js.get_form_key()
        self.requests_params = self.js.requests_params()
        self.set_tchannel_data()

    def request(self, method, url, base_url: str = None, *args, **kwargs):
        base_url = base_url or self.base_url

        response = super().request(method, base_url + url, *args, **kwargs)

        if response.status_code >= 400:
            logger.error(f"Request {method} to {url} failed with status code {response.status_code}, "
                         f"result: {response.text}")
            raise SessionException(f"Request {method} to {url} failed with status code {response.status_code}")

        return response

    def get(self, url, base_url: str = None, *args, **kwargs):
        return self.request("GET", url, base_url, *args, **kwargs)

    def post(self, url: str, base_url: str = None, *args, **kwargs):
        return self.request("POST", url, base_url, *args, **kwargs)

    def put(self, url: str, base_url: str = None, *args, **kwargs):
        return self.request("PUT", url, base_url, *args, **kwargs)

    def delete(self, url: str, base_url: str = None, *args, **kwargs):
        return self.request("DELETE", url, base_url, *args, **kwargs)

    def patch(self, url: str, base_url: str = None, *args, **kwargs):
        return self.request("PATCH", url, base_url, *args, **kwargs)

    def set_tchannel_data(self):
        logger.info("Getting tchannel data from POE API")

        data = self.get(self.settings_url).json()

        self.tchannel_data = TchannelData(**data.get("tchannelData"))
        self.headers.update({"poe-tchannel": self.tchannel_data.channel})

        logger.info(f"Got tchannel data from POE API: {self.tchannel_data.__dict__}")

    @staticmethod
    def _construct_payload(request_params: RequestParams, variables: dict = None) -> dict:
        return dict(
            queryName=request_params.name,
            extensions=dict(hash=request_params.id),
            variables=variables or {}
        )

    def send_query(self, query: Queries, variables: dict = None, base_url: str = None, **kwargs) -> dict:
        logger.info(f"Sending query {query.value} with variables {variables}")
        base_url = base_url or self.base_url
        variables = variables or {}
        query = query.value

        if not (query_params := self.requests_params.get(query)):
            raise SessionException(f"Query {query} doesn't exist in requests params")

        payload = json.dumps(
            self._construct_payload(query_params, variables),
            separators=(",", ":")
        )

        headers = {
            "Content-Type": "application/json",
            "poe-tag-id": self.js.get_tag_id(self.form_key, payload),
            "poe-formkey": self.form_key,
        }
        [self.headers.update({name: value}) for name, value in headers.items()]

        logger.info(f"Sending query '{payload}' "
                    f"with headers {self.headers.items()}"
                    f"to {base_url}{self.gql_post_url}")

        response = self.post(self.gql_post_url, base_url, data=payload, **kwargs)

        return response.json()

    def reload_request_params(self):
        return self.js.reload_requests_params(self.get("/").text)
