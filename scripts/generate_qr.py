import json
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask

BASE_URL = "https://kr9793.github.io/SmartLocationQR/location.html?id="
LOCATIONS_FILE = "../assets/data/locations.json"
OUTPUT_FOLDER = "../QR_Codes"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
    locations = json.load(f)

locations = sorted(locations, key=lambda loc: loc["id"])

def create_labeled_qr(data, text, filename, subtitle="iSmartComp2026 - Scan for location details"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Theme colors
    bg_color = "#05070d"  # Dark background
    text_color = "#f1f5f9" # Light text
    
    # Use gradient for QR code (Cyan to Purple)
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        color_mask=HorizontalGradiantColorMask(
            back_color=(5, 7, 13),      # #05070d
            left_color=(34, 211, 238),  # #22d3ee
            right_color=(168, 85, 247)  # #a855f7
        )
    ).convert('RGB')
    
    # Calculate sizes
    qr_w, qr_h = qr_img.size
    header_h = 50  # Space for conference title at top
    footer_h = 70  # Space for location name at bottom
    
    # Create new image with extra space at top and bottom
    new_img = Image.new('RGB', (qr_w, qr_h + header_h + footer_h), bg_color)
    new_img.paste(qr_img, (0, header_h))
    
    draw = ImageDraw.Draw(new_img)
    
    # Try to load appealing fonts (Segoe UI on Windows), fallback to Arial, then default
    try:
        font_title = ImageFont.truetype("segoeuib.ttf", 28) # Segoe UI Bold (Location name)
        font_sub = ImageFont.truetype("segoeui.ttf", 20)    # Segoe UI Regular (Conference title)
    except IOError:
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 26)
            font_sub = ImageFont.truetype("arial.ttf", 18)
        except IOError:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            
    # Center header (conference title/subtitle)
    bbox_sub = draw.textbbox((0, 0), subtitle, font=font_sub)
    text_w_sub = bbox_sub[2] - bbox_sub[0]
    text_x_sub = (qr_w - text_w_sub) // 2
    text_y_sub = (header_h - (bbox_sub[3] - bbox_sub[1])) // 2  # Center vertically in header
    draw.text((text_x_sub, text_y_sub), subtitle, fill=text_color, font=font_sub)

    # Center footer (location name/text)
    bbox_title = draw.textbbox((0, 0), text, font=font_title)
    text_w_title = bbox_title[2] - bbox_title[0]
    text_x_title = (qr_w - text_w_title) // 2
    text_y_title = header_h + qr_h + 15
    draw.text((text_x_title, text_y_title), text, fill=text_color, font=font_title)
    
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
create_labeled_qr(home_url, "iSmartComp2026 Home", "QR_Homepage.png", "Scan for the main conference website")
print(f"\nCreated: QR_Homepage.png")
print(f"URL:     {home_url}")