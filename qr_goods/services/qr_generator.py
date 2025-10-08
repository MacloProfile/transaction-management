import qrcode
from io import BytesIO


def generate_qr_image(qr_link) -> BytesIO:
    img = qrcode.make(qr_link)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
