import json
import os

import qrcode

BASE_URL = "https://kr9793.github.io/SmartLocationQR/location.html?id="

LOCATIONS_FILE = "../assets/data/locations.json"
OUTPUT_FOLDER = "../QR_Codes"

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

    safe_name = name.replace(' ', '_').replace('/', '_')
    filename = f"QR_{safe_name}.png"

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
print(f"All {len(locations)} location QR codes generated!")
print("================================")

# Generate Homepage QR code
home_url = "https://kr9793.github.io/SmartLocationQR/"
qr_home = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=4
)
qr_home.add_data(home_url)
qr_home.make(fit=True)
image_home = qr_home.make_image()
home_filepath = os.path.join(OUTPUT_FOLDER, "QR_Homepage.png")
image_home.save(home_filepath)

print(f"\nCreated: QR_Homepage.png")
print(f"URL:     {home_url}")