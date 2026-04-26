import re
from typing import Optional

def extract_video_id(url: str) -> Optional[str]:
    """
    Extracts the YouTube video ID from a URL.
    """
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return match.group(1) if match else None
