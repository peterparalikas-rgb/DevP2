from typing import Dict, Optional

from .base_header import BaseHeader


class ApiKeyAuth(BaseHeader):
    """
    A class for handling API key authentication in headers.

    :ivar Optional[str] _api_key: The API key.
    :ivar str _api_key_header: The header field for the API key.
    """

    _api_key: Optional[str]
    _api_key_header: str

    def __init__(self, api_key: Optional[str], api_key_header="X-API-Key"):
        """
        Initialize the ApiKeyAuth instance.

        :param api_key: The API key, or None when the caller configured none.
        :type api_key: Optional[str]
        :param api_key_header: The header field for the API key.
        :type api_key_header: str
        """
        self._api_key = api_key
        self._api_key_header = api_key_header

    def set_value(self, value: str) -> None:
        """
        Set the value of the API key.

        :param value: The new value of the API key.
        :type value: str
        """
        self._api_key = value

    def get_value(self) -> Optional[str]:
        """
        Get the raw API key, for a scheme that carries it in the URL rather than a header.

        :return: The API key.
        :rtype: Optional[str]
        """
        return self._api_key

    def get_headers(self) -> Dict[str, str]:
        """
        Get the headers with the API key field set to the API key.

        Emits nothing when no API key was supplied. The SDK constructor installs an ApiKeyAuth
        unconditionally with ``api_key`` defaulting to ``None``, so returning it directly put a
        literal ``None`` in the headers dict. REST requests filtered that out before it reached
        ``requests``/``httpx``, but the WebSocket ``connect()`` codegen merges each auth class's
        ``get_headers()`` output directly, so a literal ``None`` header value reached
        ``websockets.connect()`` (FSDK-1950, matching the header-guard idiom from FSDK-1671).

        :return: A dictionary with the API key field set to the API key, or an empty dict when no
            API key is set.
        :rtype: Dict[str, str]
        """
        if self._api_key is None:
            return {}
        return {self._api_key_header: self._api_key}
