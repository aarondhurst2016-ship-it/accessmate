def automate_checkout(url, site="auto", address=None, payment=None):
    """
    Automate checkout for supported sites using Selenium. Prompts user for address and payment if needed.
    """
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(3)
        # Amazon checkout
        if "amazon." in url:
            try:
                # Go to basket/cart
                cart_btn = driver.find_element(By.ID, "nav-cart")
                cart_btn.click()
                time.sleep(2)
                # Proceed to checkout
                checkout_btn = driver.find_element(By.NAME, "proceedToRetailCheckout")
                checkout_btn.click()
                time.sleep(2)
                # Address and payment steps (simplified)
                engine.say("Please complete address and payment in browser window.")
                engine.runAndWait()
            except Exception:
                engine.say("Could not automate Amazon checkout.")
                engine.runAndWait()
        # eBay checkout
        elif "ebay." in url:
            try:
                cart_btn = driver.find_element(By.ID, "gh-cart-n")
                cart_btn.click()
                time.sleep(2)
                checkout_btn = driver.find_element(By.ID, "ptcBtnRight")
                checkout_btn.click()
                time.sleep(2)
                engine.say("Please complete address and payment in browser window.")
                engine.runAndWait()
            except Exception:
                engine.say("Could not automate eBay checkout.")
                engine.runAndWait()
        else:
            engine.say("Site not supported for checkout automation.")
            engine.runAndWait()
        time.sleep(2)
        driver.quit()
        return True
    except Exception as e:
        engine.say(f"Checkout automation error: {e}")
        engine.runAndWait()
        return False
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyttsx3
import time

engine = pyttsx3.init()

def automate_add_to_basket(url, site="auto"):
    """
    Automate adding an item to the basket using Selenium for supported sites.
    """
    try:
        # You may need to download the appropriate webdriver (e.g., ChromeDriver)
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        # Amazon example
        if "amazon." in url:
            try:
                add_btn = driver.find_element(By.ID, "add-to-cart-button")
                add_btn.click()
                engine.say("Item added to Amazon basket.")
                engine.runAndWait()
            except Exception:
                engine.say("Could not find Amazon add to cart button.")
                engine.runAndWait()
        # eBay example
        elif "ebay." in url:
            try:
                add_btn = driver.find_element(By.ID, "atcRedesignId_btn")
                add_btn.click()
                engine.say("Item added to eBay basket.")
                engine.runAndWait()
            except Exception:
                engine.say("Could not find eBay add to basket button.")
                engine.runAndWait()
        # Walmart example
        elif "walmart." in url:
            try:
                add_btn = driver.find_element(By.CSS_SELECTOR, "button.prod-ProductCTA--primary")
                add_btn.click()
                engine.say("Item added to Walmart basket.")
                engine.runAndWait()
            except Exception:
                engine.say("Could not find Walmart add to basket button.")
                engine.runAndWait()
        # AliExpress example
        elif "aliexpress." in url:
            try:
                add_btn = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart")
                add_btn.click()
                engine.say("Item added to AliExpress basket.")
                engine.runAndWait()
            except Exception:
                engine.say("Could not find AliExpress add to basket button.")
                engine.runAndWait()
        else:
            engine.say("Site not supported for automation.")
            engine.runAndWait()
        time.sleep(2)
        driver.quit()
        return True
    except Exception as e:
        engine.say(f"Automation error: {e}")
        engine.runAndWait()
        return False
