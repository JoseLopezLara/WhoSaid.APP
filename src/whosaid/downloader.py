import re
import os
import json
import concurrent.futures
from youtube_transcript_api import (
    YouTubeTranscriptApi, 
    TranscriptsDisabled, 
    NoTranscriptFound,
    YouTubeTranscriptApiException
)
from .proxy_config import ProxyManager

class TranscriptDownloader:
    """Handles downloading and persisting YouTube transcripts."""
    
    def __init__(self, languages=['es', 'en'], proxy_count=10):
        self.languages = languages
        self.proxy_manager = ProxyManager(count=proxy_count)

    @staticmethod
    def extract_video_id(url: str) -> str:
        """Extracts the YouTube video ID from a URL."""
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
        return match.group(1) if match else None

    def download_video_transcript(self, url: str, creator: str, output_base_dir: str):
        """Downloads a video transcript using rotating proxies and selective retries."""
        video_id = self.extract_video_id(url)
        if not video_id:
            return {"status": "error", "message": f"Could not extract ID from URL: {url}"}

        max_retries = 3
        attempt = 0
        
        # Total attempts = original (0) + retries (max_retries)
        while attempt <= max_retries:
            # Always get a fresh proxy URL for each attempt
            proxy_url = self.proxy_manager.get_next_proxy_url()
            proxy_config = self.proxy_manager.get_proxy_config(proxy_url)
            api = YouTubeTranscriptApi(proxy_config=proxy_config)
            
            try:
                # Log current attempt and proxy usage
                retry_msg = f" (Retry {attempt}/{max_retries})" if attempt > 0 else ""
                print(f"Processing {url}{retry_msg} using proxy: {proxy_url}")
                
                fetched_transcript = api.fetch(
                    video_id, 
                    languages=self.languages 
                )
                transcript = fetched_transcript.to_raw_data()

                # Save transcript
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

                self.proxy_manager.wait_random()
                return {"status": "success", "video_id": video_id, "creator": creator, "path": output_file}

            except (TranscriptsDisabled, NoTranscriptFound) as e:
                # Terminal errors: no transcripts available, no point in retrying with another IP
                print(f"Video {url} has no transcripts available: {type(e).__name__}")
                self.proxy_manager.wait_random()
                return {"status": "error", "message": f"Transcripts not available for {url}"}
            
            except Exception as e:
                # Recoverable errors (IP block, connection error, etc.)
                attempt += 1
                if attempt <= max_retries:
                    print(f"Recoverable error for {url} ({type(e).__name__}). Rotating proxy...")
                    self.proxy_manager.wait_random()
                else:
                    self.proxy_manager.wait_random()
                    return {"status": "error", "message": f"Max retries reached for {url}. Last error type: {type(e).__name__} Full error type: \n {str(e)}\ln"}

    def run(self, url_dict: dict, output_base_dir: str, num_threads: int = 1):
        """Executes mass download in parallel (num_threads=1 recommended for proxy health)."""
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(self.download_video_transcript, url, creator, output_base_dir) 
                for url, creator in url_dict.items()
            ]
            
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res["status"] == "success":
                    print(f"Success: Transcript of '{res['creator']}' saved in {res['path']}")
                else:
                    print(f"Failed: {res['message']}")
                results.append(res)
        
        return results
