import random
from django.core.cache import cache

def generate_otp(length = 6):
    return str(random.randint(10**(length-1), 10**length-1))

def store_otp(user_id, otp, expiry = 300):
    cache.set(f"user_otp_{user_id}", otp, timeout=expiry)

def get_stored_otp(user_id):
    return cache.get(f"user_otp_{user_id}")

def clear_stored_otp(user_id):
    cache.delete(f"user_otp_{user_id}")
