# Configuration specific to the yt-dlp library

YDL_OPTS_BASE = {
    'skip_download': True,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'quiet': True,
    'no_warnings': True,
    'noprogress': True,
    # Evasion and Spoofing
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    },
    # Use specific clients to bypass "Proof of Origin" tokens
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web'],
            'player_skip': ['webpage', 'configs'],
        }
    },
}

def get_ydl_opts(languages):
    """Returns a copy of YDL_OPTS_BASE with specific languages."""
    opts = YDL_OPTS_BASE.copy()
    opts['subtitleslangs'] = languages
    return opts
