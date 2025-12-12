import os
import django
from django.conf import settings

# Force DEBUG=True before setup
os.environ['DJANGO_SETTINGS_MODULE'] = 'automax.settings'
# We need to hack settings after setup or just rely on env?
# Best way is to mock settings or set env before setup.
# But settings.py reads env.

import sys

def run():
    django.setup()
    from django.conf import settings
    # Force DEBUG to True for this process
    settings.DEBUG = True
    
    from django.test import Client
    from django.contrib.auth.models import User
    
    c = Client()
    
    # Try to find a user to login
    user = User.objects.first()
    if not user:
        print("No users found!")
        return

    print(f"Logging in as {user.username}...")
    c.force_login(user)
    
    print("Requesting /home/...")
    try:
        response = c.get('/home/', HTTP_HOST='127.0.0.1')
        print(f"Status Code: {response.status_code}")
        if response.status_code == 500:
            print("Response Content (First 2000 chars):")
            # In DEBUG=True, content is the traceback page
            # We can use a helper to extract the exception
            print(response.content.decode('utf-8')[:2000])
        elif response.status_code == 200:
             print("Success! Page loaded.")
        else:
            print(f"Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"Exception during request: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run()
