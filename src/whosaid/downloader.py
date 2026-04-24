import re
import os
import json
import concurrent.futures
from youtube_transcript_api import YouTubeTranscriptApi

class TranscriptDownloader:
    """Clase encargada de descargar y persistir las transcripciones de YouTube."""
    
    def __init__(self, languages=['es', 'en']):
        self.languages = languages
        self.api = YouTubeTranscriptApi()

    @staticmethod
    def extract_video_id(url):
        """Extrae el ID del video de YouTube desde la URL."""
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
        return match.group(1) if match else None

    def download_video_transcript(self, url, creator, output_base_dir):
        """Descarga la transcripción de un video y la guarda en un JSON."""
        video_id = self.extract_video_id(url)
        if not video_id:
            return {"status": "error", "message": f"No se pudo extraer el ID de la URL: {url}"}

        try:
            fetched_transcript = self.api.fetch(video_id, languages=self.languages)
            transcript = fetched_transcript.to_raw_data()

            # Estructura de carpetas por creador
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

            return {"status": "success", "video_id": video_id, "creator": creator, "path": output_file}

        except Exception as e:
            return {"status": "error", "message": f"Error procesando {url}: {str(e)}"}

    def run(self, url_dict, output_base_dir, num_threads=4):
        """Ejecuta la descarga masiva en paralelo."""
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
                    print(res["message"])
                results.append(res)
        
        return results
