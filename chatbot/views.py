import json
import os
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
from django.db.models import Q
from main.models import Listing
from main.consts import CARS_BRANDS
from .preprocessing import clean_up_sentence # Helper needed if used in views, primarily used in pipeline though

@csrf_exempt
def predict_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            
            # Get the app config instance where the model is stored
            chatbot_config = apps.get_app_config('chatbot')
            model = chatbot_config.model
            le = chatbot_config.le
            
            # Load intents (could also be cached in AppConfig)
            intents_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'intents.json')
            with open(intents_path, 'r') as f:
                intents_json = json.load(f)

            # Lazy load model if not ready (e.g. server started before training)
            if not model or not le:
                import pickle
                import sys
                from chatbot import preprocessing
                
                # Hack: Sklearn pickle expects 'preprocessing' module at top level
                if 'preprocessing' not in sys.modules:
                    sys.modules['preprocessing'] = preprocessing

                base_dir = os.path.dirname(os.path.abspath(__file__))
                model_path = os.path.join(base_dir, 'chatbot_model.pkl')
                le_path = os.path.join(base_dir, 'label_encoder.pkl')
                
                if os.path.exists(model_path) and os.path.exists(le_path):
                    with open(model_path, 'rb') as f:
                        model = pickle.load(f)
                    with open(le_path, 'rb') as f:
                        le = pickle.load(f)
                    # Cache it back to config
                    chatbot_config.model = model
                    chatbot_config.le = le
                else:
                     return JsonResponse({'answer': "I am still learning (Model not found). Please ask admin to run train.py."})

            # Prediction Logic (adapted from chat.py)
            # Reusing the pipeline from the pickle
            
            # Sklearn pipeline expects list
            probas = model.predict_proba([message])[0]
            
            ERROR_THRESHOLD = 0.25
            results = []
            for idx, prob in enumerate(probas):
                if prob > ERROR_THRESHOLD:
                    results.append({
                        "intent": le.inverse_transform([idx])[0],
                        "probability": float(prob)
                    })
            results.sort(key=lambda x: x["probability"], reverse=True)
            
            if results:
                tag = results[0]['intent']
                
                # --- Database Integration ---
                if tag == 'ask_brand_model':
                    found_brand = None
                    # Simple extraction: check if any brand name is in the message
                    # We iterate over CARS_BRANDS (tuple of code, name)
                if tag == 'ask_brand_model':
                    found_brand = None
                    import difflib
                    
                    # 1. Create a list of all valid brand names/codes to check against
                    brand_map = {}
                    for code, name in CARS_BRANDS:
                        brand_map[code.lower()] = code
                        brand_map[name.lower()] = code
                        # Aliases
                        if 'mercedes' in name.lower():
                            brand_map['mercedes'] = code
                            brand_map['merc'] = code

                    # 2. Check for direct hits in the message
                    words = message.lower().split()
                    for word in words:
                        if word in brand_map:
                            found_brand = brand_map[word]
                            break
                    
                    # 3. If no direct hit, try fuzzy matching each word against known brands
                    if not found_brand:
                        all_brands = list(brand_map.keys())
                        for word in words:
                            matches = difflib.get_close_matches(word, all_brands, n=1, cutoff=0.7)
                            if matches:
                                found_brand = brand_map[matches[0]]
                                break

                    if found_brand:
                        listings = Listing.objects.filter(brand=found_brand).order_by('-created_at')[:3]
                        if listings.exists():
                            count = Listing.objects.filter(brand=found_brand).count()
                            response_text = f"I found {count} {found_brand.title()}(s) for you:<br>"
                            for listing in listings:
                                # Clean format: "Toyota Corolla" (Title Case)
                                brand_display = listing.brand.title()
                                model_display = listing.model.title()
                                display_name = f"{brand_display} {model_display}"
                                # Dedup if model already contains brand (e.g. "BMW BMW X5")
                                if brand_display.lower() in model_display.lower():
                                    display_name = model_display
                                
                                response_text += f"🚗 <a href='/listing/{listing.id}' target='_blank' style='color: #007bff; text-decoration: none;'>{display_name}</a><br>💰 Rs. {listing.price:,}<br>"
                            
                            # Add "View All" link
                            # Assuming standard django-filter url: /?brand=found_brand
                            response_text += f"<br>👉 <a href='/?brand={found_brand}' target='_blank' style='font-weight: bold;'>View all {found_brand.title()}s</a>"
                            
                            return JsonResponse({'answer': response_text})
                        else:
                            return JsonResponse({'answer': f"Sorry, I don't see any {found_brand.title()} listings right now."})
                    else:
                        return JsonResponse({'answer': "I couldn't identify the car brand. Please check the spelling (e.g., 'Toyota', 'BMW')."})
                
                elif tag == 'ask_price_range':
                    # Extract numbers for simplistic "under X" logic
                    import re
                    # Look for "under X" or "below X" where X is a number
                    match = re.search(r'(under|below)\s+(\d+)', message.lower())
                    if match:
                        try:
                            max_price = int(match.group(2))
                            # Handle "million" / "lakh" naturally if user typed pure numbers
                            # If user typed "5 million", this regex won't catch "million". 
                            # Let's keep it simple: assume raw numbers first or improve regex later.
                            # Enhancing regex for "5 million":
                            
                            limit = max_price
                            if "million" in message.lower():
                                limit = limit * 1000000
                            elif "lakh" in message.lower() or "lakhs" in message.lower():
                                limit = limit * 100000
                                
                            listings = Listing.objects.filter(price__lte=limit, price__gt=0).order_by('price')[:3]
                            if listings.exists():
                                response_text = f"Here are some cars under Rs. {limit:,}:<br>"
                                for listing in listings:
                                    response_text += f"- <a href='/listing/{listing.id}'>{listing.brand} {listing.model}</a>: Rs. {listing.price:,}<br>"
                                return JsonResponse({'answer': response_text})
                            else:
                                 return JsonResponse({'answer': f"I couldn't find any cars under Rs. {limit:,}."})
                        except ValueError:
                            pass
                    else:
                        return JsonResponse({'answer': "I didn't catch the price limit. Try saying 'under 5000000'."})

                # --- End Database Integration ---

                for intent in intents_json['intents']:
                    if intent['tag'] == tag:
                        response = random.choice(intent['responses'])
                        return JsonResponse({'answer': response})
            
            return JsonResponse({'answer': "I'm not sure I understand. Can you rephrase?"})

        except Exception as e:
            print(f"Error in predict_view: {e}")
            with open('chatbot_debug.log', 'w') as f:
                f.write(f"Error: {str(e)}\n")
                import traceback
                f.write(traceback.format_exc())
            return JsonResponse({'answer': f"Sorry, I encountered an error: {str(e)}"}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
