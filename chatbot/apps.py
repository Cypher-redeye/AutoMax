import os
import pickle
import nltk
from django.apps import AppConfig
from django.conf import settings

class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'
    model = None
    le = None
    intents = None

    def ready(self):
        # Prevent re-loading in autoreloader thread
        if os.environ.get('RUN_MAIN') != 'true':
            return

        print("🤖 Initializing Chatbot...")
        
        # Paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'chatbot_model.pkl')
        le_path = os.path.join(base_dir, 'label_encoder.pkl')
        
        # 1. Download NLTK data (if needed)
        try:
            nltk.data.find('corpora/wordnet')
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK data...")
            nltk.download('punkt')
            nltk.download('wordnet')
            nltk.download('omw-1.4')

        # 2. Load Model & Artifacts
        if os.path.exists(model_path) and os.path.exists(le_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(le_path, 'rb') as f:
                    self.le = pickle.load(f)
                print("✅ Chatbot Model Loaded!")
            except Exception as e:
                print(f"❌ Error loading chatbot model: {e}")
        else:
            print(f"⚠️ Chatbot model not found at {model_path}. Please run train.py.")
