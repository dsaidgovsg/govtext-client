from typing import Optional, Tuple

import requests
from requests.models import Response

from govtext_client.common.configurations import AUTH_API_VERSION, CORE_API_VERSION
from govtext_client.common.constants import ContentType, Environment, ServerType
from govtext_client.common.exceptions import ClientError
from govtext_client.common.settings import Settings


class Client:
    def __init__(
        self,
        environment: Environment = Environment.PRODUCTION,
        auth_server_url: Optional[str] = None,
        core_server_url: Optional[str] = None,
        auth_api_version: Optional[str] = AUTH_API_VERSION,
        core_api_version: Optional[str] = CORE_API_VERSION,
    ):
        settings = Settings.ENVIRONMENT[environment]
        self._auth_server_url = (
            auth_server_url
            if auth_server_url is not None
            else settings[ServerType.AUTH]["url"]
        )
        self._core_server_url = (
            core_server_url
            if core_server_url is not None
            else settings[ServerType.CORE]["url"]
        )

        self._auth_api_version = auth_api_version
        self._core_api_version = core_api_version

    ########################
    # Auth (keys)
    ########################

    def get_keys(self, id: str) -> Tuple[dict, int]:
        url = "{}{}{}".format(self._auth_server_url, self._auth_api_version, "/keys/")
        headers = self._make_headers(ContentType.JSON)
        response = self._get(url, headers=headers)
        return self._parse_json_response(response)

    def get_key(self, id: str) -> Tuple[dict, int]:
        url = "{}{}{}{}".format(
            self._auth_server_url, self._auth_api_version, "/keys/", id
        )
        headers = self._make_headers(ContentType.JSON)
        response = self._get(url, headers=headers)
        return self._parse_json_response(response)

    ########################
    # Auth (users)
    ########################

    def signup(self, email: str, password: str, display_name: str) -> Tuple[dict, int]:
        data = {
            "user": {"email": email, "password": password, "display_name": display_name}
        }
        url = "{}{}{}".format(
            self._auth_server_url, self._auth_api_version, "/users/signup/"
        )
        headers = self._make_headers(ContentType.JSON)
        response = self._post(url, headers=headers, json=data)
        return self._parse_json_response(response)

    def verify_email(self, email_token: str) -> Tuple[dict, int]:
        url = "{}{}{}".format(
            self._auth_server_url, self._auth_api_version, "/users/verify_email/"
        )
        headers = self._make_headers(ContentType.JSON, token=email_token)
        response = self._post(url, headers=headers)
        return self._parse_json_response(response)

    def login(self, email: str, password: str) -> Tuple[dict, int]:
        data = {"user": {"email": email, "password": password,}}
        url = "{}{}{}".format(
            self._auth_server_url, self._auth_api_version, "/users/login/"
        )
        headers = self._make_headers(ContentType.JSON)
        response = self._post(url, headers=headers, json=data)
        return self._parse_json_response(response)

    ########################
    # Helper
    ########################

    def _make_headers(
        self, content_type: ContentType, token: Optional[str] = None
    ) -> dict:
        headers = {}
        if token:
            headers["Authorization"] = "Bearer " + token

        headers["Content-Type"] = content_type.value
        return headers

    def _get(self, url: str, headers: dict = {}, params: dict = {}) -> Response:
        try:
            response = requests.get(url, headers=headers, params=params)
        except requests.exceptions.ConnectionError:
            raise ClientError("Encounted a problem with networking.")
        except requests.exceptions.Timeout:
            raise ClientError("Requests has timed out.")
        except requests.exceptions.RequestException:
            raise ClientError("Unexpected error when making HTTP requests.")
        return response

    def _post(
        self,
        url: str,
        headers: dict = {},
        files: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Response:
        try:
            response = requests.post(
                url, headers=headers, data=data, json=json, files=files,
            )
        except requests.exceptions.ConnectionError:
            raise ClientError("Encounted a problem with networking.")
        except requests.exceptions.Timeout:
            raise ClientError("Requests has timed out.")
        except requests.exceptions.RequestException:
            raise ClientError("Unexpected error when making HTTP requests.")
        return response

    def _put(
        self,
        url: str,
        headers: dict = {},
        files: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Response:
        try:
            response = requests.put(
                url, headers=headers, data=data, json=json, files=files,
            )
        except requests.exceptions.ConnectionError:
            raise ClientError("Encounted a problem with networking.")
        except requests.exceptions.Timeout:
            raise ClientError("Requests has timed out.")
        except requests.exceptions.RequestException:
            raise ClientError("Unexpected error when making HTTP requests.")
        return response

    def _delete(self, url: str, headers: dict = {},) -> Response:
        try:
            response = requests.delete(url, headers=headers)
        except requests.exceptions.ConnectionError:
            raise ClientError("Encounted a problem with networking.")
        except requests.exceptions.Timeout:
            raise ClientError("Requests has timed out.")
        except requests.exceptions.RequestException:
            raise ClientError("Unexpected error when making HTTP requests.")
        return response

    def _parse_json_response(self, response: Response) -> Tuple[dict, int]:
        return (response.json(), response.status_code)
