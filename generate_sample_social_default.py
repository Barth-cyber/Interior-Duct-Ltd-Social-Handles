#!/usr/bin/env python
import json, urllib.parse, os
import qrcode
from PIL import Image

def main():
    defaultLinks = [
        { 'platform': 'whatsapp', 'url': 'https://wa.me/c/2348036850229' },
        { 'platform': 'instagram', 'url': 'https://www.instagram.com/interiorductltd/' },
        { 'platform': 'tiktok', 'url': 'https://www.tiktok.com/@interiorductltd' },
        { 'platform': 'facebook', 'url': 'https://www.facebook.com/interior.duct.ltd/' },
        { 'platform': 'twitter', 'url': 'https://x.com/InteriorDuctLtd' },
        { 'platform': 'youtube', 'url': 'https://www.youtube.com/@InteriorDuctLtd' },
        { 'platform': 'linkedin', 'url': 'https://www.linkedin.com/company/interior-duct-ltd/' }
    ]
    links_json = json.dumps([{'label': l.get('platform'), 'platform': l.get('platform'), 'url': l.get('url')} for l in defaultLinks])
    base = 'https://barth-cyber.github.io/idl.app'
    scan_url = base + '?links=' + urllib.parse.quote(links_json, safe='')

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
    qr.add_data(scan_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white').convert('RGB')
    img = img.resize((400,400))
    os.makedirs('assets', exist_ok=True)
    path = os.path.join('assets','sample_social_qr_default.png')
    img.save(path)
    print('WROTE', path)

if __name__ == '__main__':
    main()
