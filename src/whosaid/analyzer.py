import os
import json
import concurrent.futures
from .processor import TextProcessor

class NgramAnalyzer:
    """Clase encargada de analizar n-gramas y generar métricas de Unión/Intersección."""
    
    def __init__(self, intersection_threshold=0.6, processor=None):
        self.intersection_threshold = intersection_threshold
        self.processor = processor or TextProcessor()

    def analyze_creator(self, creator, input_base_dir, n_phrases=10, use_stopwords_filter=True):
        """Procesa todos los JSON de un creador y genera n-gramas."""
        creator_folder = os.path.join(input_base_dir, "processed_transcriptions", creator)
        if not os.path.exists(creator_folder):
            return None, None

        json_files = [f for f in os.listdir(creator_folder) if f.endswith('.json')]
        total_videos = len(json_files)
        if total_videos == 0:
            return None, None

        creator_results = {i: {} for i in range(2, 7)}

        for file_name in json_files:
            file_path = os.path.join(creator_folder, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                transcript = data['transcript']
                url = data['url']
                video_id = data['video_id']

                tokens = self.processor.tokenize_transcript(transcript)
                total_tokens = len(tokens)

                for n in range(2, 7):
                    for i in range(total_tokens - n + 1):
                        ngram_tokens = tokens[i:i+n]
                        ngram_words = tuple(t['word'] for t in ngram_tokens)

                        if not self.processor.is_valid_ngram(ngram_words, use_stopwords_filter):
                            continue

                        ngram_str = " ".join(ngram_words)
                        start_time = ngram_tokens[0]['start']
                        end_time = ngram_tokens[-1]['end']
                        appearance = {'start': start_time, 'end': end_time, 'url': url}

                        if ngram_str in creator_results[n]:
                            creator_results[n][ngram_str]['count'] += 1
                            creator_results[n][ngram_str]['video_appearances'].add(video_id)
                            creator_results[n][ngram_str]['appearances'].append(appearance)
                        else:
                            creator_results[n][ngram_str] = {
                                'count': 1,
                                'video_appearances': {video_id},
                                'start': start_time,
                                'end': end_time,
                                'url': url,
                                'appearances': [appearance]
                            }
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

        # Separar en Union e Interseccion
        min_videos_required = total_videos * self.intersection_threshold
        union_results = {i: [] for i in range(2, 7)}
        intersection_results = {i: [] for i in range(2, 7)}

        for n in range(2, 7):
            all_ngrams = []
            intersect_ngrams = []
            
            for ngram_str, info in creator_results[n].items():
                videos_count = len(info['video_appearances'])
                clean_info = {k: v for k, v in info.items() if k != 'video_appearances'}
                
                all_ngrams.append((ngram_str, clean_info))
                if videos_count >= min_videos_required:
                    intersect_ngrams.append((ngram_str, clean_info))

            all_ngrams.sort(key=lambda x: x[1]['count'], reverse=True)
            intersect_ngrams.sort(key=lambda x: x[1]['count'], reverse=True)
            
            union_results[n] = all_ngrams[:n_phrases]
            intersection_results[n] = intersect_ngrams[:n_phrases]

        return creator, {'union': union_results, 'intersection': intersection_results}

    def format_results(self, creator_results, mode):
        """Formatea los resultados para 'first_appearance' o 'all_appearances'."""
        formatted = {}
        for n in range(2, 7):
            formatted[f"{n}_grams"] = []
            for phrase, info in creator_results.get(n, []):
                count = info['count']
                if mode == 'first_appearance':
                    formatted[f"{n}_grams"].append({
                        'phrase': phrase,
                        'repetitions': count,
                        'first_appearance': {'start': info['start'], 'end': info['end'], 'url': info['url']}
                    })
                else:
                    formatted[f"{n}_grams"].append({
                        'phrase': phrase,
                        'repetitions': count,
                        'appearances': info.get('appearances', [])
                    })
        return formatted

    def run_batch_analysis(self, creators, input_base_dir, n_phrases=10, num_threads=4, use_stopwords_filter=True):
        """Ejecuta el análisis masivo por creador en paralelo."""
        top_results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(self.analyze_creator, creator, input_base_dir, n_phrases, use_stopwords_filter) 
                for creator in creators
            ]
            for future in concurrent.futures.as_completed(futures):
                creator, res = future.result()
                if creator and res:
                    top_results[creator] = res
        return top_results
