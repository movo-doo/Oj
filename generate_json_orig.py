import json
import os

image_dir = "images"
output_file = "images_collection.json"

extensions = (".jpg", ".jpeg", ".png", ".gif")

files = [
    f for f in os.listdir(image_dir)
    if f.lower().endswith(extensions)
]

files.sort()

with open(output_file, "w") as f:
    json.dump(files, f, indent=2)

print(f"{len(files)} images written to {output_file}")
