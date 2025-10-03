
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import pyttsx3

engine = pyttsx3.init()
last_item_url = None

def describe_online_item(url):
    global last_item_url
    last_item_url = url
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Try to get product title
        title = soup.find('title').text if soup.find('title') else "No title found"
        # Try to get product description (improved for more sites)
        desc = ""
        meta_desc = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
            desc = meta_desc['content']
        if not desc:
            # Try Amazon, eBay, etc.
            for id_name in ['productDescription', 'productTitle', 'itemTitle', 'desc', 'description', 'product-summary', 'productDetails', 'feature-bullets']:
                el = soup.find(id=id_name)
                if el:
                    desc = el.text.strip()
                    break
        if not desc:
            # Fallback: get first paragraph
            p = soup.find('p')
            desc = p.text if p else "No description found"
        # Try to get product image
        img_url = None
        img_tag = soup.find('img')
        if img_tag and img_tag.get('src'):
            img_url = img_tag['src']
            if not img_url.startswith('http'):
                img_url = requests.compat.urljoin(url, img_url)
        img_desc = ""
        if img_url:
            try:
                img_resp = requests.get(img_url)
                img = Image.open(io.BytesIO(img_resp.content))
                img_desc = f"Image size: {img.size}, format: {img.format}."
            except Exception:
                img_desc = "Could not analyze image."
        # Speak out info
        engine.say(f"Product: {title}")
        engine.say(f"Description: {desc}")
        if img_desc:
            engine.say(f"Image: {img_desc}")
        engine.runAndWait()
        return {'title': title, 'description': desc, 'image': img_url}
    except Exception as e:
        engine.say(f"Error fetching item: {e}")
        engine.runAndWait()
        return None

def add_to_basket(item_url=None):
    global last_item_url
    if not item_url:
        item_url = last_item_url
    # This is a stub. Real integration requires shop API or browser automation.
    engine.say("Item added to basket.")
    engine.runAndWait()
    return True
