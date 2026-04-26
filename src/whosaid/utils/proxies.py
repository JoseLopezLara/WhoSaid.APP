import random
import time
import threading
from typing import List, Optional
from youtube_transcript_api.proxies import GenericProxyConfig

class ProxyManager:
    """Manages a pool of rotating Tor proxies in a thread-safe manner."""
    
    def __init__(self, start_port: int = 8118, count: int = 10, host: str = "127.0.0.1"):
        self.proxies = [
            f"http://{host}:{port}" for port in range(start_port, start_port + count)
        ]
        self.current_index = 0
        self.wait_range = (5.0, 15.0)
        self.lock = threading.Lock()

    def get_next_proxy_url(self) -> str:
        """Retrieves the next proxy URL and increments the counter safely."""
        with self.lock:
            proxy_url = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
            return proxy_url

    def get_proxy_config(self, proxy_url: str) -> GenericProxyConfig:
        """Generates the proxy configuration for the API from a URL."""
        return GenericProxyConfig(
            http_url=proxy_url,
            https_url=proxy_url
        )

    def wait_random(self):
        """Applies a random wait time between 5 and 15 seconds."""
        wait_time = random.uniform(*self.wait_range)
        time.sleep(wait_time)
