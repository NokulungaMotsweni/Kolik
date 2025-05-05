import requests
from django.conf import settings

def verify_recaptcha_v3(token, threshold=0.5):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': settings.RECAPTCHA_V3_SECRET_KEY,
        'response': token
    }
    response = requests.post(url, data=data)
    result = response.json()
    return result.get('success', False), result.get('score', 0)

def verify_recaptcha_v2(token):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': settings.RECAPTCHA_V2_SECRET_KEY,
        'response': token
    }
    response = requests.post(url, data=data)
    result = response.json()
    return result.get('success', False)