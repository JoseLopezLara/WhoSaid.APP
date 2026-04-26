import json

class YouTubeTranscriptParser:
    """Handles parsing and selecting the best transcript from YouTube's raw metadata."""
    
    @staticmethod
    def get_best_subtitle_url(info: dict, preferred_langs: list) -> tuple:
        """Finds the best available subtitle URL (manual or automatic) in the preferred languages."""
        subtitles = info.get('subtitles', {})
        auto_captions = info.get('automatic_captions', {})

        for source in [subtitles, auto_captions]:
            for lang in preferred_langs:
                if lang in source:
                    formats = source[lang]
                    # Prefer 'json3' format
                    json3_sub = next((f['url'] for f in formats if f.get('ext') == 'json3' or 'json3' in f.get('url', '')), None)
                    if json3_sub:
                        return json3_sub, lang
                    return formats[0]['url'], lang
        return None, None

    @staticmethod
    def parse_json3(raw_json: dict) -> list:
        """Transforms YouTube's JSON3 format into our internal format."""
        transcript = []
        if 'events' in raw_json:
            for event in raw_json['events']:
                if 'segs' in event:
                    text = "".join([seg['utf8'] for seg in event['segs'] if 'utf8' in seg]).strip()
                    if not text:
                        continue
                        
                    start = event.get('tStartMs', 0) / 1000.0
                    duration = event.get('dDurationMs', 0) / 1000.0
                    
                    transcript.append({
                        "text": text,
                        "start": start,
                        "duration": duration
                    })
        return transcript
