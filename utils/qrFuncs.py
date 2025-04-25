from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO io

def get_img(file):
    return Image.open(BytesIO(file.read()))

def scan_qr(file):
    img = get_img(file)

    decoded_objects = decode(img)

    if not decoded_objects:
        return None

    qr_data = [obj.data.decode('utf-8') for obj in decoded_objects]
    
    return qr_data