
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automax.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import Listing

# 1. Print all users and their listing counts
print("Current Users and Listing Counts:")
for u in User.objects.all():
    count = u.profile.listing_set.count()
    print(f"- User: {u.username} (Listings: {count})")

# 2. Delete testuser if exists
try:
    user = User.objects.get(username='testuser')
    print(f"\nDeleting 'testuser' and their {user.profile.listing_set.count()} listings...")
    user.delete()
    print("Deleted 'testuser'.")
except User.DoesNotExist:
    print("\nUser 'testuser' not found.")

# 3. Check if there are other suspicious listings (optional)
remaining = Listing.objects.count()
print(f"\nRemaining Total Listings: {remaining}")
