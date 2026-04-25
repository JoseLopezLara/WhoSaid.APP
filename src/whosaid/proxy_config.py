import random
import time
from typing import List, Optional
from youtube_transcript_api.proxies import GenericProxyConfig

class ProxyManager:
    """Gestiona un pool de proxies Tor rotativos."""
    
    def __init__(self, start_port: int = 8118, count: int = 10, host: str = "127.0.0.1"):
        self.proxies = [
            f"http://{host}:{port}" for port in range(start_port, start_port + count)
        ]
        self.current_index = 0
        self.wait_range = (5.0, 15.0)

    def get_next_proxy_config(self) -> GenericProxyConfig:
        """Obtiene la configuración del siguiente proxy en el pool (Round Robin)."""
        proxy_url = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        
        return GenericProxyConfig(
            http_url=proxy_url,
            https_url=proxy_url
        )

    def wait_random(self):
        """Aplica un tiempo de espera aleatorio entre 5 y 15 segundos."""
        wait_time = random.uniform(*self.wait_range)
        time.sleep(wait_time)
