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
    """Clase encargada de descargar y persistir las transcripciones de YouTube."""
    
    def __init__(self, languages=['es', 'en'], proxy_count=10):
        self.languages = languages
        self.proxy_manager = ProxyManager(count=proxy_count)

    @staticmethod
    def extract_video_id(url):
        """Extrae el ID del video de YouTube desde la URL."""
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
        return match.group(1) if match else None

    def download_video_transcript(self, url, creator, output_base_dir):
        """Descarga la transcripción de un video con rotación de proxies y reintentos selectivos."""
        video_id = self.extract_video_id(url)
        if not video_id:
            return {"status": "error", "message": f"No se pudo extraer el ID de la URL: {url}"}

        max_retries = 3
        attempts = 0
        
        while attempts <= max_retries:
            proxy_config = self.proxy_manager.get_next_proxy_config()
            api = YouTubeTranscriptApi(proxy_config=proxy_config)
            
            try:
                fetched_transcript = api.fetch(
                    video_id, 
                    languages=self.languages, 
                )

                transcript = fetched_transcript.to_raw_data()

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
                # Caso donde no tiene sentido reintentar (sin subtítulos)
                print(f"Video {url} no tiene transcripciones disponibles: {str(e)}")
                self.proxy_manager.wait_random()
                return {"status": "error", "message": f"Transcripciones no disponibles para {url}"}
            
            except Exception as e:
                # Cualquier otro error (bloqueo de IP, timeout, etc.) se reintenta
                attempts += 1
                if attempts <= max_retries:
                    print(f"Error recuperable en {url} ({type(e).__name__}) (IP: {proxy_config.http_url}) . Reintento {attempts}/{max_retries} con nuevo proxy...")
                    self.proxy_manager.wait_random()
                else:
                    self.proxy_manager.wait_random()
                    return {"status": "error", "message": f"Máximos reintentos agotados para {url}. Último error: {str(e)}"}

    def run(self, url_dict, output_base_dir, num_threads=1):
        """
        Ejecuta la descarga masiva. 
        Nota: num_threads se reduce a 1 por defecto para respetar la lógica de rotación secuencial y esperas,
        pero se mantiene el parámetro por compatibilidad.
        """
        results = []
        # Debido a la naturaleza de la rotación de proxies y esperas aleatorias solicitadas,
        # el procesamiento secuencial es más seguro para evitar bloqueos masivos, 
        # pero mantenemos el executor con control de hilos.
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
