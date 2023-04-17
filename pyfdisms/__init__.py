import logging
import re
import sys
import requests
from typing import (
    Optional, Dict, Any, List, Tuple
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


class SmsClient:
    """
    FDI SMS Client
    """

    SANDBOX_BASE_URL: str = "https://messaging-sandbox.fdibiz.com"
    PRODUCTION_BASE_URL: str = "https://messaging.fdibiz.com"

    def __init__(
        self, *, api_key: str, api_secret: str, sandbox: Optional[bool] = True
    ):
        """
        Initializes the SMS client with provided API key, API secret, and base URL.

        Args:
            api_key (str): The API key used for authentication.
            api_secret (str): The API secret used for authentication.
            sandbox (Optional[bool], optional): Determines whether to use the
                sandbox environment. Defaults to True.

        Attributes:
            BASE_URL (str): The base URL (either sandbox or production) for API calls.
            _api_key (str): The API key used for authentication.
            _api_secret (str): The API secret used for authentication.
            _access_token (str): The access token used for API calls.
            _refresh_token (str): The refresh token used for refreshing access tokens.
        """

        if sandbox:
            self.BASE_URL = self.SANDBOX_BASE_URL

        self._api_key: str = api_key
        self._api_secret: str = api_secret
        self._access_token: str
        self._refresh_token: str

        self._access_token, self.__refresh_token = self._tokens()

    def _tokens(self) -> Tuple:
        """
        Retrieves and returns the access token and refresh token for the API.

        The method sends a POST request to the authentication URL with the API key and secret in the body.
        If the request is successful, the method returns a tuple containing the access and refresh tokens.

        Returns:
            Tuple: A tuple containing the access token (str) and the refresh token (str).
        """

        url: str = f"{self.BASE_URL}/api/v1/auth/"
        resp: Dict[str, Any] = self._post(
            url=url,
            body={
                "api_username": self._api_key,
                "api_password": self._api_secret,
            },
            _headers=False,
        )
        if resp["success"]:
            access_token = resp.get("access_token")
            refresh_token = resp.get("refresh_token")
        return access_token, refresh_token

    def refresh(self) -> None:
        """
        Refreshes the API access token using the refresh token.

        This method sends a POST request to the refresh URL with the refresh token in the body.
        If the request is successful, the method updates the access_token and refresh_token attributes.
        """
        url: str = f"{self.BASE_URL}/api/v1/auth/refresh"
        resp: Dict[str, Any] = self._post(
            url=url,
            body={
                "refresh_token": self._refresh_token
            },
            _headers=False,
        )
        if resp["success"]:
            self._access_token = resp.get("access_token")
            self._refresh_token = resp.get("refresh_token")
        return

    @property
    def _headers(self) -> Dict[str, str]:
        """
        Generates and returns authenticated headers for API requests.

        The headers include authentication "Authorization" and "Content-Type" keys.

        Returns:
            Dict[str, str]: A dictionary containing authenticated headers.
        """

        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

    def _get(self, url: str, params: Dict[Any, Any] = None, _headers: bool = True) -> Dict[str, Any]:
        """
        Sends a GET request to the specified URL with optional parameters and headers.

        Args:
            url (str): The URL for the API endpoint.
            params (Dict[Any, Any], optional): A dictionary of key-value pairs to include in the
                request's query parameters. Defaults to None.
            _headers (bool, optional): A flag to determine whether custom headers from the
                "_headers" property should be included in the request. Defaults to True.
        Returns:
            Dict[str, Any]: The response JSON as a Python dictionary.
        """

        if not _headers:
            resp = requests.get(
                url=url,
                params=params,
                headers={"Content-Type": "application/json"},
            )
        else:
            resp = requests.get(
                url=url, params=params, headers=self._headers
            )

        if resp.status_code == 200:
            return resp.json()
        else:
            if "success" in resp.json():
                return resp.json()
            else:
                return {
                    "success": False,
                    "status": resp.status_code,
                    "message": resp.text,
                }

    def _post(
        self, url: str, body: Dict[Any, Any], _headers: bool = True
    ) -> Dict[str, Any]:
        """
        Sends a POST request to the specified URL with the given body and optional headers.

        Args:
            url (str): The URL for the API endpoint.
            body (Dict[Any, Any]): A dictionary of key-value pairs to include in the
                request's body as JSON.
            _headers (bool, optional): A flag to determine whether custom headers from the
                "_headers" property should be included in the request. Defaults to True.


        Returns:
            Dict[str, Any]: The response JSON as a Python dictionary.
        """
        if not _headers:
            resp = requests.post(
                url=url,
                json=body,
                headers={"Content-Type": "application/json"},
            )
        else:
            resp = requests.post(
                url=url, json=body, headers=self._headers
            )

        return resp.json()

    def _clean_mobile_number(self, mobile_number: str) -> str:
        """
        Cleans and formats the given mobile number.

        Args:
            mobile_number (str): The mobile number to be cleaned and formatted.

        Returns:
            str: A cleaned and formatted mobile number with the default country code (Rwanda) if not provided.

        Raises:
            ValueError: If the mobile number length is less than 9 or greater than 12 after cleaning.
        """
        # remove any non-numeric characters
        mobile_number = re.sub(r"[^0-9]", "", mobile_number)
        if len(mobile_number) < 9 or len(mobile_number) > 12:
            raise ValueError("Invalid mobile number")

        # default country is Rwanda
        if len(mobile_number) == 9:
            mobile_number = f"250{mobile_number}"
        elif len(mobile_number) == 10:
            mobile_number = mobile_number.replace("0", "250", 1)
        return mobile_number

    def check_health(self) -> Dict[str, Any]:
        """
        Checks the API health status by sending a GET request to the status endpoint.

        Sends a GET request to the status endpoint and returns the response as a dictionary.

        Returns:
            Dict[str, Any]: A dictionary containing the health status data of the API, including
                a "success" key (bool) that indicates whether the request was successful.
        """
        url: str = f"{self.BASE_URL}/api/v1/status"

        resp: Dict[str, Any] = self._get(
            url=url,
            _headers=False,
        )
        return resp

    def balance(self) -> Dict[str, Any]:
        """
        Retrieves the current credit balance from the API.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the API.
        """
        url: str = f"{self.BASE_URL}/api/v1/balance/now"
        resp: Dict[str, Any] = self._get(
            url=url,
        )

        return resp

    def balance_on_date(self, date_string: str) -> Dict[str, Any]:
        """
        Retrieves the credit balance at any point in time.

        Args:
            date_string (str): The date string in the format YYYY-MM-DD.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the API.
        """
        url: str = f"{self.BASE_URL}/api/v1/balance/{date_string}/closing"
        resp: Dict[str, Any] = self._get(
            url=url,
        )

        return resp

    def send_single(self, *, msisdn: str, message: str, msg_ref: str, sender_id: str = None, callback_url: str = None) -> Dict[str, Any]:
        """
        Send a message to a single MSISDN.

        Args:
            msisdn (str): The mobile number to send the message to.
            message (str): The content of the message.
            msg_ref (str): A unique reference for the message.
            sender_id (str, optional): The sender ID for the message. Defaults to None.
            callback_url (str, optional): A callback URL for delivery reports. Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the API.
        """
        msisdn = self._clean_mobile_number(msisdn)
        url: str = f"{self.BASE_URL}/api/v1/mt/single"
        body: Dict[str, Any] = {
            "msisdn": msisdn,
            "message": message,
            "msgRef": msg_ref,
            "sender_id": sender_id,
            "dlr": callback_url,
        }

        resp: Dict[str, Any] = self._post(
            url=url,
            body=body,
        )

        return resp

    def send_bulk(self, *, msisdn_list: List, message: str, msg_ref: str, sender_id: str = None, callback_url: str = None) -> Dict[str, Any]:
        """
        Send a message to a list of MSISDNs.

        Args:
            msisdn_list (list): The mobile number to send the message to.
            message (str): The content of the message.
            msg_ref (str): A unique reference for the message.
            sender_id (str, optional): The sender ID for the message. Defaults to None.
            callback_url (str, optional): A callback URL for delivery reports. Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the API.
        """
        cleaned_msisdns: List = []
        for no in msisdn_list:
            cleaned_msisdns.append(self._clean_mobile_number(no))

        url: str = f"{self.BASE_URL}/api/v1/mt/single"
        body: Dict[str, Any] = {
            "msisdn": cleaned_msisdns,
            "message": message,
            "msgRef": msg_ref,
            "sender_id": sender_id,
            "dlr": callback_url,
        }

        resp: Dict[str, Any] = self._post(
            url=url,
            body=body,
        )

        return resp

    def get_stats(self) -> Dict[str, Any]:
        """
        Get status for MT (mobile terminated) and MO (mobile originated) messages for
        today (Central African Time).

        Returns:
            Dict[str, Any]: A dictionary containing the response from the API.
        """

        url: str = f"{self.BASE_URL}/api/v1/stats"
        resp: Dict[str, Any] = self._get(
            url=url
        )

        return resp

    def get_stats_on_date(self, date_string: str) -> Dict[str, Any]:
        """
        Get status for MT (mobile terminated) and MO (mobile originated) messages for
        a specific date.

        Args:
            date_string (str): The date string in the format YYYY-MM-DD.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the API.
        """

        url: str = f"{self.BASE_URL}/api/v1/stats/{date_string}"
        resp: Dict[str, Any] = self._get(
            url=url
        )

        return resp

    def validate_msisdn(self, msisdn: str, country_code: str) -> Dict[str, Any]:
        """
        Check whether an MSISDN is valid for a specific country.

        Args:
            msisdn (str): The mobile number to validate.
            country_code (str): Two character ISO 3361-1 country code.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the API.
        """

        msisdn = self._clean_mobile_number(msisdn)
        country_code = country_code.upper()

        url: str = f"{self.BASE_URL}/api/v1/validate/msisdn"
        body: Dict[str, str] = {
            "msisdn": msisdn,
            "countryCode": country_code
        }

        resp: Dict[str, Any] = self._post(
            url=url,
            body=body
        )

        return resp

    def validate_msisdn_bulk(self, msisdn_list: List, country_code: str) -> Dict[str, Any]:
        """
        Check whether a list of MSISDN is valid for a specific country.

        Args:
            msisdn (str): The mobile number to validate.
            country_code (str): Two character ISO 3361-1 country code.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the API.
        """

        cleaned_msisdns: List = []
        for no in msisdn_list:
            cleaned_msisdns.append(self._clean_mobile_number(no))

        country_code = country_code.upper()

        url: str = f"{self.BASE_URL}/api/v1/validate/msisdn/bulk"
        body: Dict[str, str] = {
            "msisdn_list": msisdn_list,
            "countryCode": country_code
        }

        resp: Dict[str, Any] = self._post(
            url=url,
            body=body
        )

        return resp
