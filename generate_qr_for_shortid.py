import os
import qrcode
from qrcode.image.svg import SvgImage
from PIL import Image
from reportlab.pdfgen import canvas

short_id='idl1'
url=f"https://barth-cyber.github.io/idl-social-handles/idl.app?id={short_id}"
out='assets'
os.makedirs(out, exist_ok=True)
png=os.path.join(out,f'short_{short_id}.png')
svg=os.path.join(out,f'short_{short_id}.svg')
pdf=os.path.join(out,f'short_{short_id}.pdf')
qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)
img=qr.make_image(fill_color='black', back_color='white').convert('RGB')
img=img.resize((600,600), Image.LANCZOS)
img.save(png)
print('WROTE',png)
factory=SvgImage
svg_img=qrcode.make(url, image_factory=factory)
svg_img.save(svg)
print('WROTE',svg)
im=Image.open(png)
w,h=im.size
c=canvas.Canvas(pdf,pagesize=(w,h))
c.drawImage(png,0,0,width=w,height=h)
c.showPage(); c.save()
print('WROTE',pdf)
