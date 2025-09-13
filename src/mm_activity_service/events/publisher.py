import json
import logging
import requests

from abc import ABC, abstractmethod
from typing import Any
import threading
from mm_activity_service.config.config import Config
from mm_activity_service.events.models import ActivityEvent, RatedEvent, WatchlistedEvent

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
        self.timeout = 2.0

    def start(self) -> None:
        logger.info("Dapr publisher ready (multi-topic mode: rated='%s', watchlisted='%s')",
                    self.cfg.DAPR_RATED_TOPIC, self.cfg.DAPR_WATCHLISTED_TOPIC)

    def stop(self) -> None:
        pass

    def _get_topic_for_event(self, event: ActivityEvent) -> str:
        if isinstance(event, RatedEvent):
            return self.cfg.DAPR_RATED_TOPIC
        elif isinstance(event, WatchlistedEvent):
            return self.cfg.DAPR_WATCHLISTED_TOPIC
        # fallback for generic base events:
        elif getattr(event, "action", None) == "RATED":
            return self.cfg.DAPR_RATED_TOPIC
        elif getattr(event, "action", None) == "WATCHLISTED":
            return self.cfg.DAPR_WATCHLISTED_TOPIC
        return self.cfg.DAPR_PUBSUB_TOPIC

    def publish(self, event: ActivityEvent) -> None:
        main_topic = self._get_topic_for_event(event)
        self._publish_to_topic(main_topic, event)

        #Publish to the fallback topic as ActivityEvent (base fields only)
        fallback_topic = self.cfg.DAPR_PUBSUB_TOPIC
        if fallback_topic != main_topic:
            # Always downcast to base ActivityEvent for the fallback topic
            base_event = ActivityEvent(
                userId=event.userId,
                movieId=event.movieId,
                action=event.action,
                timestamp=event.timestamp,
            )
            self._publish_to_topic(fallback_topic, base_event)

    def _publish_to_topic(self, topic: str, event: ActivityEvent) -> None:
        raw_q = "?metadata.rawPayload=true" if self.cfg.DAPR_PUBSUB_RAWPAYLOAD else ""
        base_url = (
            f"http://{self.cfg.DAPR_HOST}:{self.cfg.DAPR_HTTP_PORT}"
            f"/v1.0/publish/{self.cfg.DAPR_PUBSUB_NAME}/{topic}{raw_q}"
        )
        payload = event.to_dict()
        headers = {
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(
                base_url,
                data=json.dumps(payload),
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            logger.debug("Published event to topic '%s': %s", topic, payload)
        except Exception as e:
            logger.error(f"Failed to publish event to Dapr topic {topic}: {e} | payload={payload}")
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