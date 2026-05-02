import os
import qrcode
from qrcode.image.svg import SvgImage

try:
    import cairosvg
except Exception:
    cairosvg = None

short_id = 'yklwu8'
base = 'https://barth-cyber.github.io/interiorductltd.app'
scan_url = base + f'?id={short_id}'

out_dir = 'assets'
os.makedirs(out_dir, exist_ok=True)

# PNG (600x600) - high quality
png_path = os.path.join(out_dir, 'sample_social_qr_short.png')
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(scan_url)
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white').convert('RGB')
img = img.resize((600,600))
img.save(png_path)
print('WROTE', png_path)

# SVG
svg_path = os.path.join(out_dir, 'sample_social_qr_short.svg')
factory = SvgImage
svg_img = qrcode.make(scan_url, image_factory=factory)
svg_img.save(svg_path)
print('WROTE', svg_path)

# PDF via cairosvg if available
pdf_path = os.path.join(out_dir, 'sample_social_qr_short.pdf')
if cairosvg is not None:
    with open(svg_path, 'rb') as f:
        svg_bytes = f.read()
    cairosvg.svg2pdf(bytestring=svg_bytes, write_to=pdf_path)
    print('WROTE', pdf_path)
else:
    print('cairosvg not installed; skipping PDF (run: pip install cairosvg)')
