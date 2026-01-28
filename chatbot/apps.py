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
        def load_model():
            if os.path.exists(model_path) and os.path.exists(le_path):
                try:
                    with open(model_path, 'rb') as f:
                        self.model = pickle.load(f)
                    with open(le_path, 'rb') as f:
                        self.le = pickle.load(f)
                    print("✅ Chatbot Model Loaded!")
                    return True
                except Exception as e:
                    print(f"❌ Error loading chatbot model: {e}")
            return False

        if not load_model():
            print("⚠️ Model missing or incompatible. Retraining...")
            try:
                from chatbot.train import train_model
                train_model()
                print("✅ Retraining complete. Attempting to load...")
                load_model()
            except Exception as e:
                print(f"❌ Training failed: {e}")
