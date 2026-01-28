import json
import pickle
import random
import nltk
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
try:
    from chatbot.preprocessing import clean_up_sentence
except ImportError:
    from preprocessing import clean_up_sentence

# ... (rest of imports)

def train_model():
    # Load intents
    base_dir = os.path.dirname(os.path.abspath(__file__))
    intents_path = os.path.join(base_dir, 'data', 'intents.json')

    try:
        with open(intents_path, 'r') as file:
            intents = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find intents.json at {intents_path}")
        return

    # Prepare training data
    patterns = []
    tags = []

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            patterns.append(pattern)
            tags.append(intent['tag'])

# Encode labels
    le = LabelEncoder()
    y = le.fit_transform(tags)

    # Build Pipeline: TF-IDF -> Logistic Regression
    # We use our custom 'clean_up_sentence' from preprocessing.py as the tokenizer
    pipe = Pipeline([
        ('vectorizer', TfidfVectorizer(tokenizer=clean_up_sentence, token_pattern=None)), 
        ('classifier', LogisticRegression(C=10, max_iter=1000))
    ])

    # Train
    print("Training model...")
    pipe.fit(patterns, y)

    # Save artifacts
    print("Saving artifacts...")
    model_path = os.path.join(base_dir, 'chatbot_model.pkl')
    le_path = os.path.join(base_dir, 'label_encoder.pkl')

    with open(model_path, 'wb') as f:
        pickle.dump(pipe, f)

    with open(le_path, 'wb') as f:
        pickle.dump(le, f)

    print("✅ Model trained and saved successfully (Scikit-Learn)!")

if __name__ == "__main__":
    train_model()
