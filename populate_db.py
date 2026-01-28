
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automax.settings')
django.setup()

from main.models import Listing
from users.models import Profile, Location
from django.contrib.auth.models import User

# Ensure we have a user/profile
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('password')
    user.save()
profile, created = Profile.objects.get_or_create(user=user)
if created:
    location = Location.objects.create(address="Colombo", city="Colombo", zip_code="00100")
    profile.location = location
    profile.save()

brands = ['toyota', 'bmw', 'honda', 'nissan', 'suzuki', 'mercedes']
models_map = {
    'toyota': ['Corolla', 'Camry', 'Prius', 'Vitz'],
    'bmw': ['3 Series', '5 Series', 'X5', 'i8'],
    'honda': ['Civic', 'Fit', 'Vezel', 'Accord'],
    'nissan': ['Leaf', 'Sunny', 'Patrol'],
    'suzuki': ['Wagon R', 'Alto', 'Swift'],
    'mercedes': ['C-Class', 'E-Class', 'S-Class']
}

print("Creating dummy listings...")
for brand in brands:
    for model in models_map.get(brand, []):
        price = random.randint(2000000, 15000000)
        Listing.objects.create(
            seller=profile,
            brand=brand,
            model=model,
            vin=f"VIN{random.randint(1000,9999)}",
            mileage=random.randint(10000, 100000),
            color="Black",
            description=f"A nice {brand} {model}.",
            engine="2.0L",
            transmission="automatic",
            price=price
        )
        print(f"Created {brand} {model} - Rs. {price}")

print("Done!")
