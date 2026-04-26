import sys
import os
from typing import Dict, List, Any

# Ensure the 'src' directory is in the python path
sys.path.append(os.path.abspath("src"))

from whosaid import TranscriptDownloader, NgramAnalyzer, StorageManager
from whosaid.config.analysis import INTERSECTION_THRESHOLD, DEFAULT_N_PHRASES
from whosaid.config.base import DEBUG, ENVIRONMENT

# ==============================================================================
# RUNTIME CONFIGURATION
# ==============================================================================
NUM_THREADS: int = 1
OUTPUT_DIR: str = "processed_files"

# Test data mapping URLs to Creators
TEST_DICTIONARY: Dict[str, str] = {
    "https://www.youtube.com/watch?v=mJcJ0ikucOY": "XOCAS",
    "https://www.youtube.com/watch?v=aMcTiuqqJas": "GUSGRI",
    #"https://www.youtube.com/watch?v=kewy2RUYb3c": "XOCAS",
    #"https://www.youtube.com/watch?v=n9RhsFlKeSI": "XOCAS",
    #"https://www.youtube.com/watch?v=S8q9eHBnHxE": "XOCAS",
    #"https://www.youtube.com/watch?v=dnWT6lV8Zms": "GUSGRI",
    #"https://www.youtube.com/watch?v=yUAbe5isKTg": "GUSGRI",
    #"https://www.youtube.com/watch?v=5rF-0wK4fpI": "GUSGRI",
    #"https://www.youtube.com/watch?v=R2BYWHmhBuk": "GUSGRI",
    #"https://www.youtube.com/watch?v=8V6b5hCx5F8": "XOCAS",
    #"https://www.youtube.com/watch?v=tf4LAo_JY68": "XOCAS",
    #"https://www.youtube.com/watch?v=Bfy1yDB_YXM": "XOCAS",
    #"https://www.youtube.com/watch?v=JaqdFMzWmqU": "XOCAS",
    #"https://www.youtube.com/watch?v=tUsXRMXlHl0": "GUSGRI",
    #"https://www.youtube.com/watch?v=PYPsdJmcgjo": "GUSGRI",
    #"https://www.youtube.com/watch?v=i49LvJMtwbM": "GUSGRI",
    #"https://www.youtube.com/watch?v=p5jo4kS2P8Q": "GUSGRI",
    #"https://www.youtube.com/watch?v=fQxVMOSB_L8": "GUSGRI",
    #"https://www.youtube.com/watch?v=SOnBk94vOzk": "GUSGRI",
    #"https://www.youtube.com/watch?v=-ibeiAm_VEY": "GUSGRI"
}

def run_orchestration() -> None:
    """
    Main orchestration flow for downloading transcripts and analyzing n-grams.
    """
    print(f"--- Starting WhoSaid.APP Orchestration ({ENVIRONMENT}) ---")
    if DEBUG:
        print("[DEBUG MODE ENABLED]")
    
    # 1. Initialize Managers
    storage = StorageManager(base_dir=OUTPUT_DIR)
    downloader = TranscriptDownloader(languages=['es', 'en'])
    # Se inicializa con los defaults del archivo de config
    analyzer = NgramAnalyzer(intersection_threshold=INTERSECTION_THRESHOLD)

    # 2. Setup Directories
    print(f"Setting up directories in: {OUTPUT_DIR}")
    storage.setup_directories()

    # 3. Stage 1: Download Transcripts
    print("\n[Stage 1] Downloading Transcripts...")
    downloader.run(TEST_DICTIONARY, output_base_dir=OUTPUT_DIR, num_threads=NUM_THREADS)

    # 4. Stage 2: Analyze N-grams
    print("\n[Stage 2] Running N-gram Analysis...")
    creators: List[str] = list(set(TEST_DICTIONARY.values()))
    results: Dict[str, Any] = analyzer.run_batch_analysis(
        creators, 
        input_base_dir=OUTPUT_DIR, 
        n_phrases=DEFAULT_N_PHRASES, 
        num_threads=NUM_THREADS
    )

    # 5. Save Results
    print("\n[Stage 3] Saving Results...")
    storage.save_results(results, analyzer)
    
    print("\n--- Orchestration Completed Successfully ---")

if __name__ == "__main__":
    try:
        run_orchestration()
    except Exception as e:
        print(f"\n[ERROR] Orchestration failed: {e}")
        sys.exit(1)
