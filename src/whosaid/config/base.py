import os
from typing import Optional

def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """Retrieves a secret from environment variables."""
    return os.getenv(key, default)

# General environment settings
DEBUG = get_secret("DEBUG", "False").lower() == "true"
ENVIRONMENT = get_secret("ENVIRONMENT", "development")
