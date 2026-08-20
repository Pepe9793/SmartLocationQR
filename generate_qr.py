import qrcode
import os

BASE_URL = "https://pepe9793.github.io/SmartLocationQR/location.html?id="

OUTPUT_FOLDER = "QR_Codes"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for location_id in range(1, 17):

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
    print(f"URL: {url}")
    print()

print("================================")
print("All 16 QR codes generated!")
print("================================")