import json
import logging
import requests

from abc import ABC, abstractmethod
from typing import Any
import threading
from mm_activity_service.config.config import Config
from mm_activity_service.events.models import ActivityEvent

logger = logging.getLogger(__name__)
_publisher_instance = None
_publisher_lock = threading.Lock()

class Publisher(ABC):
    @abstractmethod
    def start(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...

    @abstractmethod
    def publish(self, event: ActivityEvent) -> None:
        ...

class NoopPublisher(Publisher):
    def start(self) -> None:
        logger.info("Events disabled: NoopPublisher active")

    def stop(self) -> None:
        pass

    def publish(self, event: ActivityEvent) -> None:
        logger.debug("NOOP publish: %s", event.to_dict())

class DaprHTTPPublisher(Publisher):
    def __init__(self, cfg: Config):
        self.cfg = cfg
        # Compose query param for raw payload (Dapr docs recommend true for non-CloudEvent)
        raw_q = "?metadata.rawPayload=true" if self.cfg.DAPR_PUBSUB_RAWPAYLOAD else ""
        self.base_url = (
            f"http://{self.cfg.DAPR_HOST}:{self.cfg.DAPR_HTTP_PORT}"
            f"/v1.0/publish/{self.cfg.DAPR_PUBSUB_NAME}/{self.cfg.DAPR_PUBSUB_TOPIC}{raw_q}"
        )
        self.timeout = 2.0

    def start(self) -> None:
        logger.info("Dapr publisher targeting %s", self.base_url)

    def stop(self) -> None:
        pass

    def publish(self, event: ActivityEvent) -> None:
        payload = event.to_dict()
        headers = {
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(
                self.base_url,
                data=json.dumps(payload),
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            logger.debug("Published event: %s", payload)
        except Exception as e:
            logger.error(f"Failed to publish event to Dapr: {e} | payload={payload}")
            raise

def get_publisher(cfg: Config = None) -> Publisher:
    global _publisher_instance
    with _publisher_lock:
        if _publisher_instance is None:
            if cfg is None:
                cfg = Config()
            if cfg.EVENTS_ENABLED:
                _publisher_instance = DaprHTTPPublisher(cfg)
            else:
                _publisher_instance = NoopPublisher()
            _publisher_instance.start()
        return _publisher_instance