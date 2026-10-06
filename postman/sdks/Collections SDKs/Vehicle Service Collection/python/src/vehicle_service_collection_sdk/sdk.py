import warnings
import requests
import logging
from typing import Optional, Union
from .services.vehicle_service_collection_sdk import VehicleServiceCollectionSdkService
from .net.environment import Environment


class VehicleServiceCollectionSdk:
    """
    Main SDK client class for VehicleServiceCollectionSdk.
    Provides centralized configuration and access to all service endpoints.
    Supports authentication, environment management, and global timeout settings.
    """

    def __init__(
        self,
        *,
        api_key: str = None,
        api_key_header: str = "X-API-Key",
        base_url: Union[Environment, str, None] = None,
        timeout: float = None,
        timeout_ms: int = None,
        http_client: Optional[requests.Session] = None,
        follow_redirects: bool = True,
        logger: Optional[logging.Logger] = None,
        retry: "RetryConfig" = None,
    ):
        """
        Initializes VehicleServiceCollectionSdk the SDK class.
        """

        _resolved_url = (
            base_url.value if isinstance(base_url, Environment) else base_url
        )
        self._base_url = _resolved_url.rstrip("/") if _resolved_url else _resolved_url
        self.vehicle_service_collection_sdk = VehicleServiceCollectionSdkService(
            base_url=self._base_url,
            http_client=http_client,
            follow_redirects=follow_redirects,
            logger=logger,
        )
        self.set_api_key(api_key, api_key_header)
        if timeout_ms is not None:
            warnings.warn(
                "`timeout_ms` is deprecated; use `timeout` (in seconds) instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            timeout = timeout_ms / 1000 if timeout is None else timeout
        if timeout is None:
            timeout = 60
        self.set_timeout(timeout)
        if retry is not None:
            self.set_retry(retry)

    def set_base_url(self, base_url: Union[Environment, str]):
        """
        Sets the base URL for the entire SDK.

        :param Union[Environment, str] base_url: The base URL to be set.
        :return: The SDK instance.
        """
        _resolved_url = (
            base_url.value if isinstance(base_url, Environment) else base_url
        )
        self._base_url = _resolved_url.rstrip("/") if _resolved_url else _resolved_url

        self.vehicle_service_collection_sdk.set_base_url(self._base_url)

        return self

    def set_api_key(self, api_key: str, api_key_header="X-API-Key"):
        """
        Sets the api key and the api key header for the entire SDK.
        """
        self.vehicle_service_collection_sdk.set_api_key(api_key, api_key_header)

        return self

    def set_timeout(self, timeout: float):
        """
        Sets the timeout for the entire SDK.

        :param float timeout: The timeout (in seconds) to be set.
        :return: The SDK instance.
        """
        self.vehicle_service_collection_sdk.set_timeout(timeout)

        return self

    def set_http_client(self, http_client: Optional[requests.Session]):
        """
        Sets a custom HTTP client for the entire SDK.

        :param http_client: A requests.Session-compatible client, used as-is (the SDK never
            reconfigures its transport). Pass None to fall back to the module-level requests API.
        :return: The SDK instance.
        """
        self.vehicle_service_collection_sdk.set_http_client(http_client)

        return self

    def set_follow_redirects(self, follow_redirects: bool):
        """
        Sets whether HTTP redirects (3xx responses) are followed automatically, for the entire SDK.

        :param bool follow_redirects: False to return a 3xx response as-is instead of following it.
        :return: The SDK instance.
        """
        self.vehicle_service_collection_sdk.set_follow_redirects(follow_redirects)

        return self

    def set_logging(self, logger: Optional[logging.Logger]):
        """
        Sets the logger requests/responses are written to, for the entire SDK.

        :param logger: A standard library logger. Pass None (the default) to disable logging.
            Authorization and Cookie header values are always redacted from logged output.
        :return: The SDK instance.
        """
        self.vehicle_service_collection_sdk.set_logging(logger)

        return self

    def set_retry(self, retry: "RetryConfig"):
        """
        Sets the retry configuration for the entire SDK.

        :param RetryConfig retry: The retry configuration to be set.
        :return: The SDK instance.
        """
        self.vehicle_service_collection_sdk.set_retry(retry)

        return self


# c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
