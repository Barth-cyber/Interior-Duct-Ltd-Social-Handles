#!/usr/bin/env python
import json
import urllib.parse
import os
import sys

try:
    import qrcode
    from PIL import Image
    
    # Create sample links
    links = [
        {"label": "WhatsApp Business", "platform": "whatsapp", "url": "https://wa.me/2348036850229"},
        {"label": "Instagram Channel", "platform": "instagram", "url": "https://instagram.com/interiorductltd"}
    ]
    
    # Build the scan URL
    links_json = json.dumps(links, separators=(',', ':'))
    base = 'https://barth-cyber.github.io/idl-social-handles/idl.app'
    scan_url = base + '?links=' + urllib.parse.quote(links_json, safe='')
    
    print(f"Generated scan URL (length: {len(scan_url)})")
    
    # Create QR code
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=4
    )
    qr.add_data(scan_url)
    qr.make(fit=True)
    
    print("QR code generated")
    
    # Generate image
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Resize to 400x400
    img = img.resize((400, 400), Image.NEAREST)
    
    # Ensure assets directory exists
    os.makedirs('assets', exist_ok=True)
    
    # Save
    path = os.path.join('assets', 'sample_social_qr.png')
    img.save(path)
    
    print(f"✓ SAVED to {path}")
    print("SUCCESS")
    sys.exit(0)
    
except ImportError as e:
    print(f"Import error: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
    sys.exit(1)
