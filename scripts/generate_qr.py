import json
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "https://kr9793.github.io/SmartLocationQR/location.html?id="
LOCATIONS_FILE = "../assets/data/locations.json"
OUTPUT_FOLDER = "../QR_Codes"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
    locations = json.load(f)

locations = sorted(locations, key=lambda loc: loc["id"])

def create_labeled_qr(data, text, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Calculate sizes
    qr_w, qr_h = qr_img.size
    text_h = 70  # Space for text at the bottom
    
    # Create new image with extra space at bottom
    new_img = Image.new('RGB', (qr_w, qr_h + text_h), 'white')
    new_img.paste(qr_img, (0, 0))
    
    draw = ImageDraw.Draw(new_img)
    
    # Try to load a nice font, fallback to default
    try:
        font = ImageFont.truetype("arialbd.ttf", 26) # Arial Bold
    except IOError:
        try:
            font = ImageFont.truetype("arial.ttf", 26)
        except IOError:
            font = ImageFont.load_default()
            
    # Get text bounding box to center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    
    # If text is too wide, scale it down or just center it (it might bleed off edges)
    # We'll just center it
    text_x = (qr_w - text_w) // 2
    text_y = qr_h + 15
    draw.text((text_x, text_y), text, fill="black", font=font)
    
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    new_img.save(filepath)

for location in locations:
    location_id = location["id"]
    name = location.get("name", f"Location {location_id}")
    url = BASE_URL + str(location_id)
    
    safe_name = name.replace(' ', '_').replace('/', '_')
    filename = f"QR_{safe_name}.png"
    
    create_labeled_qr(url, name, filename)
    print(f"Created: {filename}")
    print(f"Name:    {name}")
    print(f"URL:     {url}\n")

print("================================")
print(f"All {len(locations)} location QR codes generated!")
print("================================")

# Generate Homepage QR code
home_url = "https://kr9793.github.io/SmartLocationQR/"
create_labeled_qr(home_url, "iSmartComp2026 Home", "QR_Homepage.png")
print(f"\nCreated: QR_Homepage.png")
print(f"URL:     {home_url}")