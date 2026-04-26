import os
import json
import time
import random
import concurrent.futures
import yt_dlp
import requests

from whosaid.config.yt_dlp import get_ydl_opts
from whosaid.utils.helpers import extract_video_id
from .parsers import YouTubeTranscriptParser

class TranscriptDownloader:
    """Orchestrates downloading and persisting YouTube transcripts."""
    
    def __init__(self, languages=['es', 'en']):
        self.languages = languages
        self.ydl_opts = get_ydl_opts(self.languages)
        self.parser = YouTubeTranscriptParser()
        # Extract headers from config for consistent requests
        self.headers = self.ydl_opts.get('http_headers', {})

    def _fetch_content(self, subtitle_url: str) -> list:
        """Helper to fetch and parse transcript content."""
        response = requests.get(subtitle_url, headers=self.headers, timeout=10)
        response.raise_for_status()
        
        try:
            return self.parser.parse_json3(response.json())
        except (json.JSONDecodeError, KeyError):
            return []

    def download_video_transcript(self, url: str, creator: str, output_base_dir: str):
        """Downloads a video transcript with retry pattern and human-like behavior."""
        video_id = extract_video_id(url)
        if not video_id:
            return {"status": "error", "message": f"Could not extract ID from URL: {url}"}

        max_retries = 2
        attempt = 0
        
        while attempt <= max_retries:
            try:
                retry_msg = f" (Retry {attempt}/{max_retries})" if attempt > 0 else ""
                print(f"Processing {url}{retry_msg} using yt-dlp...")
                
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    sub_url, _ = self.parser.get_best_subtitle_url(info, self.languages)
                    
                    if not sub_url:
                        return {"status": "error", "message": f"Transcripts not available for {url}"}

                    transcript = self._fetch_content(sub_url)
                    
                    if not transcript:
                        return {"status": "error", "message": f"Could not parse transcript content for {url}"}

                    # Persist
                    creator_folder = os.path.join(output_base_dir, "processed_transcriptions", creator)
                    os.makedirs(creator_folder, exist_ok=True)
                    output_file = os.path.join(creator_folder, f"{video_id}.json")

                    data = {
                        "creator": creator,
                        "url": url,
                        "video_id": video_id,
                        "transcript": transcript
                    }

                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

                    time.sleep(random.uniform(90, 120))
                    return {"status": "success", "video_id": video_id, "creator": creator, "path": output_file}

            except Exception as e:
                attempt += 1
                if attempt <= max_retries:
                    time.sleep(random.uniform(90, 120))
                else:
                    return {"status": "error", "message": f"Max retries reached: {type(e).__name__}"}

    def run(self, url_dict: dict, output_base_dir: str, num_threads: int = 1):
        """Executes mass download in parallel."""
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(self.download_video_transcript, url, creator, output_base_dir) 
                for url, creator in url_dict.items()
            ]
            
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                status = "Success" if res["status"] == "success" else "Failed"
                msg = res.get('path', res.get('message'))
                print(f"{status}: {msg}")
                results.append(res)
        
        return results
