"""
wardrobe.py - Personal wardrobe and style assistant
- Store clothing items and style preferences
- Suggest outfits based on your style, weather, and events
"""
import json
import os

WARDROBE_FILE = "wardrobe_data.json"

class Wardrobe:
    def __init__(self):
        self.items = []
        self.style = {
            "preferred_styles": [],  # e.g., ["casual", "formal", "sporty"]
            "favorite_colors": [],
            "favorite_brands": [],
        }
        self.load()

    def add_item(self, name, type_, color, brand, tags=None):
        self.items.append({
            "name": name,
            "type": type_,
            "color": color,
            "brand": brand,
            "tags": tags or []
        })
        self.save()

    def remove_item(self, name):
        self.items = [item for item in self.items if item["name"] != name]
        self.save()

    def set_style(self, preferred_styles=None, favorite_colors=None, favorite_brands=None):
        if preferred_styles is not None:
            self.style["preferred_styles"] = preferred_styles
        if favorite_colors is not None:
            self.style["favorite_colors"] = favorite_colors
        if favorite_brands is not None:
            self.style["favorite_brands"] = favorite_brands
        self.save()

    def suggest_outfit(self, weather=None, event=None):
        # Simple suggestion: match preferred style, color, brand
        suggestions = []
        for item in self.items:
            if (not self.style["preferred_styles"] or item["type"] in self.style["preferred_styles"]) and \
               (not self.style["favorite_colors"] or item["color"] in self.style["favorite_colors"]) and \
               (not self.style["favorite_brands"] or item["brand"] in self.style["favorite_brands"]):
                suggestions.append(item)
        if not suggestions:
            suggestions = self.items  # fallback: show all
        return suggestions

    def list_items(self):
        return self.items

    def save(self):
        with open(WARDROBE_FILE, "w", encoding="utf-8") as f:
            json.dump({"items": self.items, "style": self.style}, f, indent=2)

    def load(self):
        if os.path.exists(WARDROBE_FILE):
            with open(WARDROBE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.items = data.get("items", [])
                self.style = data.get("style", self.style)

if __name__ == "__main__":
    wardrobe = Wardrobe()
    print("Wardrobe assistant. Commands: add, remove, setstyle, suggest, list, quit")
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "quit":
            break
        elif cmd == "add":
            name = input("Name: ")
            type_ = input("Type (e.g., shirt, pants): ")
            color = input("Color: ")
            brand = input("Brand: ")
            tags = input("Tags (comma separated): ").split(",")
            wardrobe.add_item(name, type_, color, brand, [t.strip() for t in tags if t.strip()])
        elif cmd == "remove":
            name = input("Name to remove: ")
            wardrobe.remove_item(name)
        elif cmd == "setstyle":
            styles = input("Preferred styles (comma): ").split(",")
            colors = input("Favorite colors (comma): ").split(",")
            brands = input("Favorite brands (comma): ").split(",")
            wardrobe.set_style([s.strip() for s in styles if s.strip()],
                              [c.strip() for c in colors if c.strip()],
                              [b.strip() for b in brands if b.strip()])
        elif cmd == "suggest":
            print("Suggested outfits:")
            for item in wardrobe.suggest_outfit():
                print(item)
        elif cmd == "list":
            print("Your wardrobe:")
            for item in wardrobe.list_items():
                print(item)
        else:
            print("Commands: add, remove, setstyle, suggest, list, quit")
