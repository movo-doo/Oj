import os
import json
import re

IMAGE_FOLDER = "images"
JSON_FILE = "json_images.json"
CATEGORIES_FILE = "json_categories.json"

# Supported image extensions
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")


def normalize_text(text):
    return re.sub(r"\s+", " ", text.lower().replace("_", " ")).strip()


def extract_categories_from_filename(filename, normalized_categories):
    name = os.path.splitext(filename)[0]

    normalized_name = normalize_text(name)

    matched = set()

    for key, original in normalized_categories.items():
        if key in normalized_name:
            matched.add(original)

    if not matched:
        matched.add("Uncategorized")

    return list(matched)


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

            categories = extract_categories_from_filename(filename, normalized_categories)

            data.append({
                "file": filename,
                "categories": categories
            })

# Save updated JSON
with open(JSON_FILE, "w") as f:
    json.dump(data, f, indent=2)

print("Done updating json_images.json")