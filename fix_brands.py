
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automax.settings')
django.setup()

from main.models import Listing

# Fix 'mercedes' -> 'mercedes benz'
count = Listing.objects.filter(brand='mercedes').update(brand='mercedes benz')
print(f"Updated {count} Mercedes listings.")
