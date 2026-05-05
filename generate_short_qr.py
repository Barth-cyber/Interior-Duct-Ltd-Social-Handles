import os
import qrcode
from PIL import Image

short_id = 'yklwu8'
base = 'https://barth-cyber.github.io/idl.app'
scan_url = base + f'?id={short_id}'

out_dir = 'assets'
os.makedirs(out_dir, exist_ok=True)
path = os.path.join(out_dir, 'sample_social_qr_short.png')

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(scan_url)
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white').convert('RGB')
img = img.resize((600,600), Image.LANCZOS)
img.save(path)
print('WROTE', path)
