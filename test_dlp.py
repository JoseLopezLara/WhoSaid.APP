import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath("src"))

from whosaid import TranscriptDownloader

def test_single_download():
    downloader = TranscriptDownloader(languages=['es', 'en'])
    url = "https://www.youtube.com/watch?v=-ibeiAm_VEY"
    creator = "GUSGRI"
    output_dir = "test_output"
    
    print(f"Testing download for: {url}")
    result = downloader.download_video_transcript(url, creator, output_dir)
    
    if result["status"] == "success":
        print(f"Success! File saved at: {result['path']}")
        with open(result['path'], 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("\nStructure Check:")
            print(f"Creator: {data.get('creator')}")
            print(f"Transcript type: {type(data.get('transcript'))}")
            if data.get('transcript'):
                print(f"First entry: {data['transcript'][0]}")
    else:
        print(f"Failed: {result['message']}")

if __name__ == "__main__":
    test_single_download()
