# Outfit and recipe recommendation for Kivy (mobile/desktop)
def recommend_outfit(detected_items, weather):
    # Simple logic: if cold, suggest warm clothes; if hot, suggest light clothes
    if 'cold' in weather or 'rain' in weather:
        if 'jacket' in detected_items:
            return "Wear your jacket and pants."
        else:
            return "Wear warm clothes."
    elif 'hot' in weather or 'sun' in weather:
        if 'tshirt' in detected_items:
            return "Wear your t-shirt and shorts."
        else:
            return "Wear light clothes."
    else:
        return "Wear comfortable clothes."

def recommend_recipe(detected_food):
    # Simple logic: suggest a recipe based on detected food
    if 'apple' in detected_food:
        return "Try an apple pie recipe!"
    elif 'milk' in detected_food:
        return "Make a milkshake!"
    else:
        return "No recipe found for detected food."
