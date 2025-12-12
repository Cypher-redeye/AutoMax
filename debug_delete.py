import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automax.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from main.models import Listing

def run():
    # 1. Setup Users and Listings
    user1 = User.objects.first()
    user2 = User.objects.last()
    
    if user1 == user2:
        print("Need at least 2 users to test permissions properly.")
        user2 = User.objects.create_user(username='test_user_2', password='password')
        
    print(f"U1:{user1} U2:{user2}")
    
    # Create a listing for User1
    listing = Listing.objects.create(
        seller=user1.profile,
        brand='bmw',
        model='Test Delete Model',
        vin='123456789',
        mileage=1000,
        color='red',
        description='To be deleted',
        engine='V8',
        transmission='automatic'
    )
    c = Client()
    
    # Check URL resolution
    from django.urls import resolve
    try:
        res = resolve(f'/listing/{listing.id}/delete/')
        print(f"URL Resolve: {res.func.__name__}")
    except Exception as e:
        print(f"URL Fail: {e}")

    # Test
    c.force_login(user2)
    r1 = c.get(f'/listing/{listing.id}/delete/', follow=True, HTTP_HOST='127.0.0.1')
    print(f"R1: {r1.status_code}")
    
    if Listing.objects.filter(id=listing.id).exists():
        print("PASS: Unauth delete prevented.")
    else:
        print("FAIL: Unauth delete happened!")

    c.force_login(user1)
    r2 = c.get(f'/listing/{listing.id}/delete/', follow=True, HTTP_HOST='127.0.0.1')
    print(f"R2: {r2.status_code}")
    
    if not Listing.objects.filter(id=listing.id).exists():
        print("PASS: Auth delete success.")
    else:
        print("FAIL: Auth delete failed!")

if __name__ == '__main__':
    run()
