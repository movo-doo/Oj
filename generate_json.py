import os
import json

IMAGE_FOLDER = "images"
JSON_FILE = "json_images.json"
CATEGORIES_FILE = "json_categories.json"

# Supported image extensions
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")

# Load categories
if os.path.exists(CATEGORIES_FILE):
    with open(CATEGORIES_FILE, "r") as f:
        categories_data = json.load(f)
        category_list = categories_data.get("categories", [])
else:
    category_list = []

# Normalize categories for matching (lowercase)
normalized_categories = {cat.lower(): cat for cat in category_list}

# Load existing JSON data
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
else:
    data = []

# Create a set of existing filenames
existing_files = {item["file"] for item in data if "file" in item}

# Scan directory for images
for filename in os.listdir(IMAGE_FOLDER):
    if filename.lower().endswith(VALID_EXTENSIONS):
        if filename not in existing_files:
            print(f"Adding new image: {filename}")

            # Extract first word (before space, underscore, or dash)
            name_without_ext = os.path.splitext(filename)[0]
            first_word = name_without_ext.split()[0].split("_")[0].split("-")[0]

            # Match category (case-insensitive)
            matched_category = normalized_categories.get(first_word.lower(), "Uncategorized")

            data.append({
                "file": filename,
                "categories": [matched_category]
            })

# Save updated JSON
with open(JSON_FILE, "w") as f:
    json.dump(data, f, indent=2)

print("Done updating json_images.json")