import os
import json
import re

# ---------------- Configuration ----------------
IMAGE_FOLDER = "images"
JSON_FILE = "json_images.json"
CATEGORIES_FILE = "json_categories.json"

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")

# ---------------- Utility Functions ----------------
def normalize_text(text):
    """Lowercase, replace underscores with spaces, collapse whitespace."""
    return re.sub(r"\s+", " ", text.lower().replace("_", " ")).strip()


def build_category_maps(category_data):
    """
    Build normalized category lookup and optional catalog shortcut map.
    
    category_data: list of categories from JSON
        e.g., [["Messier","M"], ["Caldwell","C"], ["NGC"], ...]
    """
    normalized_categories = {}
    catalog_shortcuts = {}

    for entry in category_data:
        display_name = entry[0]
        normalized_name = normalize_text(display_name)
        normalized_categories[normalized_name] = display_name

        # Optional shortcut for catalog ID detection
        if len(entry) > 1:
            shortcut = entry[1].lower()
            catalog_shortcuts[shortcut] = display_name

    return normalized_categories, catalog_shortcuts


def extract_categories_from_filename(filename, normalized_categories, catalog_shortcuts):
    """
    Extract categories from filename based on:
      1. Normalized category names (compound terms handled)
      2. Catalog IDs with optional numbers (e.g., M13, C25, NGC 6205)
    """
    name = os.path.splitext(filename)[0]
    normalized_name = normalize_text(name)

    matched = set()

    # 1️⃣ Match normal categories
    for key, display in normalized_categories.items():
        if key in normalized_name:
            matched.add(display)

    # 2️⃣ Match catalog shortcuts + number
    for shortcut, display in catalog_shortcuts.items():
        pattern = rf"\b{re.escape(shortcut)}\s*\d+\b"
        if re.search(pattern, normalized_name, re.IGNORECASE):
            matched.add(display)

    # 3️⃣ Fallback if no matches
    if not matched:
        matched.add("Uncategorized")

    return list(matched)

# ---------------- Load Category Data ----------------
if os.path.exists(CATEGORIES_FILE):
    with open(CATEGORIES_FILE, "r") as f:
        categories_data = json.load(f)
        category_list = categories_data.get("categories", [])
else:
    category_list = []

# Build normalized category maps
normalized_categories, catalog_shortcuts = build_category_maps(category_list)

# ---------------- Load Existing Images ----------------
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
else:
    data = []

existing_files = {item["file"] for item in data if "file" in item}

# ---------------- Scan for New Images ----------------
for filename in os.listdir(IMAGE_FOLDER):
    if filename.lower().endswith(VALID_EXTENSIONS) and filename not in existing_files:
        categories = extract_categories_from_filename(filename, normalized_categories, catalog_shortcuts)
        print(f"Adding new image: {filename} → categories: {categories}")
        data.append({
            "file": filename,
            "categories": categories
        })

# ---------------- Save Updated JSON ----------------
with open(JSON_FILE, "w") as f:
    json.dump(data, f, indent=2)

print("Done updating json_images.json")