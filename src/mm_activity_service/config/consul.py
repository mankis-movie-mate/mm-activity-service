from logging import Logger

import requests
import time
from mm_activity_service.config.config import Config


class Consul:
    def __init__(self, logger: Logger):
        config = Config()
        self.logger = logger
        self.base_url = config.BASE_URL
        self.ds_host = config.DS_HOST
        self.ds_port = config.DS_PORT
        self.service_host = config.HOST
        self.service_port = config.PORT
        self.traefik_tags = config.LB_TAGS
        self.service_name = "mm-activity-service"
        self.service_id = f"{self.service_name}-{int(time.time())}"
        self.health_check_url = f"http://{self.service_host}:{self.service_port}/health"
        self.check_interval = "10s"

    def register_service(self) -> None:
        """Register service in Consul for service discovery."""
        consul_url = f"http://{self.ds_host}:{self.ds_port}/v1/agent/service/register"
        tags_raw = self.traefik_tags.strip()
        if tags_raw:
            # Split by lines, trim whitespace, ignore empty lines
            tags = [line.strip() for line in tags_raw.splitlines() if line.strip()]
        else:
            tags = []
        service_definition = {
            "Name": self.service_name,
            "ID": self.service_id,
            "Address": self.service_host,
            "Port": int(self.service_port),
            "Tags": tags,
            "Check": {
                "HTTP": self.health_check_url,
                "Interval": self.check_interval
            }
        }

        response = requests.put(consul_url, json=service_definition)
        if response.status_code == 200:
            self.logger.info(f"Registered service {self.service_id} with Consul at {consul_url}")
        else:
            self.logger.info(f"Failed to register service {self.service_id} with Consul. Status code: {response.status_code}, Response: {response.text}")

    def deregister_service(self) -> None:
        """Deregister service from Consul."""
        consul_url = f"http://{self.ds_host}:{self.ds_port}/v1/agent/service/deregister/{self.service_id}"

        response = requests.put(consul_url)
        if response.status_code == 200:
            self.logger.info(f"Deregistered service {self.service_id} from Consul")
        else:
            self.logger.info(f"Failed to deregister service {self.service_id} from Consul. Status code: {response.status_code}, Response: {response.text}")