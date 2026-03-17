import os
import json

IMAGE_FOLDER = "images"
JSON_FILE = "json_images.json"

# Supported image extensions
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")

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

            data.append({
                "file": filename,
                "categories": []
            })

# Save updated JSON
with open(JSON_FILE, "w") as f:
    json.dump(data, f, indent=2)

print("Done updating json_images.json")
