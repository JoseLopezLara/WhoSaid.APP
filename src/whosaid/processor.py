import string
import nltk
from nltk.corpus import stopwords

class TextProcessor:
    """Clase encargada de limpiar, tokenizar y filtrar texto de transcripciones."""
    
    def __init__(self, language='spanish'):
        self.language = language
        try:
            self.stop_words = set(stopwords.words(language))
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words(language))

    @staticmethod
    def clean_word(word):
        """Convierte a minúsculas y elimina signos de puntuación."""
        word = word.lower()
        return word.translate(str.maketrans('', '', string.punctuation))

    def is_valid_ngram(self, ngram_words, use_stopwords_filter=True):
        """
        Regla de negocio: El n-grama es descartado solo si TODAS las palabras
        que lo componen son stopwords.
        """
        if not use_stopwords_filter:
            return True

        are_all_stopwords = all(word in self.stop_words for word in ngram_words)
        return not are_all_stopwords

    def tokenize_transcript(self, transcript):
        """
        Descompone la transcripción en una lista de palabras donde cada una
        retiene el inicio (start) y el fin (end) de su bloque original.
        """
        tokens = []
        for block in transcript:
            text = block.get('text', '')
            start = block.get('start', 0)
            end = start + block.get('duration', 0)

            words = text.split()
            for p in words:
                clean_p = self.clean_word(p)
                if clean_p:
                    tokens.append({
                        'word': clean_p,
                        'start': start,
                        'end': end
                    })
        return tokens
