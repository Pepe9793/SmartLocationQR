import json
import os

import qrcode

BASE_URL = "https://pepe9793.github.io/SmartLocationQR/location.html?id="

LOCATIONS_FILE = "locations.json"
OUTPUT_FOLDER = "QR_Codes"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
    locations = json.load(f)

# Sort by id so filenames/output stay in a predictable order,
# and generate for whatever IDs currently exist in locations.json
# instead of a hardcoded range — add or remove a location there
# and this script picks it up automatically.
locations = sorted(locations, key=lambda loc: loc["id"])

for location in locations:

    location_id = location["id"]
    name = location.get("name", f"Location {location_id}")

    url = BASE_URL + str(location_id)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image()

    filename = f"QR_{location_id:02d}.png"

    filepath = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    image.save(filepath)

    print(f"Created: {filename}")
    print(f"Name:    {name}")
    print(f"URL:     {url}")
    print()

print("================================")
print(f"All {len(locations)} QR codes generated!")
print("================================")