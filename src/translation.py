# translation.py
# Translation and language learning feature

import requests

def translate(text, target_lang):
    # Use Google Translate API (or free endpoint)
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': 'auto',
        'tl': target_lang,
        'dt': 't',
        'q': text
    }
    try:
        response = requests.get(url, params=params)
        result = response.json()
        translated = result[0][0][0]
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text
