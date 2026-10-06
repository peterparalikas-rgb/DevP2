import requests
import logging
from typing import Optional, Union
from .net.environment import Environment
from .sdk import VehicleServiceCollectionSdk
from .services.async_.vehicle_service_collection_sdk import (
    VehicleServiceCollectionSdkServiceAsync,
)


class VehicleServiceCollectionSdkAsync(VehicleServiceCollectionSdk):
    """
    VehicleServiceCollectionSdkAsync is the asynchronous version of the VehicleServiceCollectionSdk SDK Client.
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
        super().__init__(
            api_key=api_key,
            api_key_header=api_key_header,
            base_url=base_url,
            timeout=timeout,
            timeout_ms=timeout_ms,
            http_client=http_client,
            follow_redirects=follow_redirects,
            logger=logger,
            retry=retry,
        )

        self.vehicle_service_collection_sdk = VehicleServiceCollectionSdkServiceAsync(
            base_url=self._base_url,
            http_client=http_client,
            follow_redirects=follow_redirects,
            logger=logger,
        )
        if retry is not None:
            self.set_retry(retry)
