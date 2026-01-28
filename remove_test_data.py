
import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automax.settings')
django.setup()

try:
    user = User.objects.get(username='testuser')
    count = user.profile.listing_set.count() # Count before delete
    print(f"Found user 'testuser' with {count} listings.")
    user.delete()
    print("Successfully deleted 'testuser' and all associated listings.")
except User.DoesNotExist:
    print("User 'testuser' not found. Maybe already deleted?")
except Exception as e:
    print(f"Error: {e}")
