import random
import os
import json
import pickle
from preprocessing import clean_up_sentence # IMPT: Required for pickle loading

# ---------------- LOAD INTENTS ----------------
try:
    with open("data/intents.json") as file:
        intents = json.load(file)
        print("DEBUG: Loaded data/intents.json")
except FileNotFoundError:
    with open("../data/intents.json") as file:
        intents = json.load(file)
        print("DEBUG: Loaded ../data/intents.json")

# ---------------- LOAD MODEL & ARTIFACTS ----------------
MODEL_PATHS = [
    "chatbot_model.pkl",
    "src/chatbot_model.pkl"
]

model = None
le = None

for path in MODEL_PATHS:
    if os.path.exists(path):
        base = os.path.dirname(path)
        print(f"DEBUG: Loading models from {base}...")
        with open(path, "rb") as f:
            model = pickle.load(f)
        with open(os.path.join(base, "label_encoder.pkl"), "rb") as f:
            le = pickle.load(f)
        print(f"DEBUG: Loaded Sklearn model from {path}")
        break

if model is None:
    raise FileNotFoundError("❌ Model files (chatbot_model.pkl) not found!")

# ---------------- PREDICTION ----------------
def predict_class(sentence):
    # Pipeline handles vectorization automatically
    # We use predict_proba to get confidence scores
    
    # Sklearn expects a list/array of strings
    probas = model.predict_proba([sentence])[0]
    
    # Get indices of top predictions
    # We want to format this similar to the old output
    ERROR_THRESHOLD = 0.25
    
    results = []
    for idx, prob in enumerate(probas):
        if prob > ERROR_THRESHOLD:
            results.append({
                "intent": le.inverse_transform([idx])[0],
                "probability": float(prob)
            })
    
    results.sort(key=lambda x: x["probability"], reverse=True)
    return results

# ---------------- RESPONSE ----------------
def get_response(intents_list, intents_json):
    if not intents_list:
        return "Sorry, I didn't understand that."

    tag = intents_list[0]["intent"]

    for intent in intents_json["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Sorry, something went wrong."

# ---------------- CLI TEST ----------------
if __name__ == "__main__":
    print("🤖 Bot is running! (Scikit-Learn Edition)")
    print("Type 'quit' to exit")

    while True:
        message = input("You: ")
        if message.lower() == "quit":
            break

        intents_list = predict_class(message)
        # Debug print
        # print(f"DEBUG intents: {intents_list}")
        
        response = get_response(intents_list, intents)
        print("Bot:", response)
