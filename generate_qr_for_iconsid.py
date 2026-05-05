import os
import qrcode
from qrcode.image.svg import SvgImage
from PIL import Image

short = 'idl_icons_v1'
base = 'https://barth-cyber.github.io/idl.app'
url = base + f'?iconsId={short}'

out = 'assets'
os.makedirs(out, exist_ok=True)

png_path = os.path.join(out, f'sample_qr_icons_{short}.png')
svg_path = os.path.join(out, f'sample_qr_icons_{short}.svg')
pdf_path = os.path.join(out, f'sample_qr_icons_{short}.pdf')

# PNG
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white').convert('RGB')
img = img.resize((600,600), Image.LANCZOS)
img.save(png_path)
print('WROTE', png_path)

# SVG
factory = SvgImage
svg_img = qrcode.make(url, image_factory=factory)
svg_img.save(svg_path)
print('WROTE', svg_path)

# PDF via reportlab if available (embed PNG)
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import landscape
    from reportlab.lib.units import inch
    img = Image.open(png_path)
    w,h = img.size
    c = canvas.Canvas(pdf_path, pagesize=(w, h))
    c.drawImage(png_path, 0, 0, width=w, height=h)
    c.showPage()
    c.save()
    print('WROTE', pdf_path)
except Exception as e:
    print('Skipping PDF (reportlab missing or error):', e)
