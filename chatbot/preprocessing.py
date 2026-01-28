import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize

# ---- Ensure required NLTK data (safe for Render) ----
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()


def clean_up_sentence(sentence: str) -> list[str]:
    """
    Tokenize and lemmatize a sentence.
    Uses wordpunct_tokenize to avoid heavy punkt dependency.
    """
    tokens = wordpunct_tokenize(sentence)
    return [lemmatizer.lemmatize(token.lower()) for token in tokens]


def bag_of_words(sentence: str, words: list[str]) -> np.ndarray:
    """
    Create a bag-of-words vector.
    1 if word exists in sentence, else 0.
    Optimized using set lookup.
    """
    sentence_words = set(clean_up_sentence(sentence))
    bag = np.zeros(len(words), dtype=np.float32)

    for idx, word in enumerate(words):
        if word in sentence_words:
            bag[idx] = 1.0

    return bag
