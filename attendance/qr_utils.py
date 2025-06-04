import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(data):
   
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)
    return File(buffer, name='qr.png')