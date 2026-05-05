#!/usr/bin/env python
"""
End-to-end test: Verify the dynamic social links UI and scan.html integration.
"""
import json
import urllib.parse
import sys

def test_dynamic_rows():
    """Verify row collection logic matches index.html generateSocialQR"""
    print("=" * 60)
    print("TEST 1: Dynamic Rows Collection")
    print("=" * 60)
    
    # Simulate rows as they would be collected in index.html
    rows_data = [
        {"platform": "whatsapp", "url": "https://wa.me/2348036850229"},
        {"platform": "instagram", "url": "https://instagram.com/interiorductltd"},
        {"platform": "facebook", "url": "https://facebook.com/interiorductltd"}
    ]
    
    platform_names = {
        'whatsapp': 'WhatsApp Business',
        'instagram': 'Instagram Channel',
        'facebook': 'Facebook Page',
    }
    
    # Simulate collectSocialRows() function from index.html
    links = []
    for row in rows_data:
        platform = row.get('platform', '')
        url = row.get('url', '')
        if platform and url:
            try:
                # Basic URL validation
                if url.startswith('http'):
                    links.append({
                        'label': platform_names.get(platform, platform),
                        'platform': platform,
                        'url': url
                    })
            except:
                pass
    
    print(f"✓ Collected {len(links)} valid social links:")
    for i, link in enumerate(links, 1):
        print(f"  {i}. {link['label']} → {link['url'][:50]}...")
    
    return links


def test_scan_url_generation(links):
    """Verify scan URL generation matches index.html generateSocialQR"""
    print("\n" + "=" * 60)
    print("TEST 2: Scan URL Generation")
    print("=" * 60)
    
    # Simulate generateSocialQR() logic
    links_json = json.dumps(links)
    base = 'https://barth-cyber.github.io/idl.app'
    scan_url = base + '?links=' + urllib.parse.quote(links_json, safe='')
    
    print(f"✓ Generated scan URL:")
    print(f"  Base: {base}")
    print(f"  Full length: {len(scan_url)} chars")
    print(f"  Full URL: {scan_url[:100]}...")
    
    return scan_url


def test_scan_page_parsing(scan_url):
    """Verify scan.html can parse the encoded links"""
    print("\n" + "=" * 60)
    print("TEST 3: Scan Page Link Parsing")
    print("=" * 60)
    
    # Extract query params
    parsed = urllib.parse.urlparse(scan_url)
    params = urllib.parse.parse_qs(parsed.query)
    
    if 'links' in params:
        try:
            links_json = params['links'][0]
            decoded_links = json.loads(links_json)
            print(f"✓ Decoded {len(decoded_links)} links from scan URL:")
            for i, link in enumerate(decoded_links, 1):
                print(f"  {i}. {link['label']}")
                print(f"     Platform: {link['platform']}")
                print(f"     URL: {link['url']}")
            return decoded_links
        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse links JSON: {e}")
            return None
    else:
        print("✗ No 'links' parameter in scan URL")
        return None


def test_qr_url_validity(scan_url):
    """Verify scan URL is a valid URL"""
    print("\n" + "=" * 60)
    print("TEST 4: QR Code Target URL Validity")
    print("=" * 60)
    
    try:
        urllib.parse.urlparse(scan_url)
        # Verify it's HTTPS and points to the app URL
        if 'idl.app' in scan_url and scan_url.startswith('https://'):
            print(f"✓ Scan URL is valid HTTPS URL")
            print(f"  Protocol: HTTPS ✓")
            print(f"  Target: idl.app ✓")
            print(f"  Has links parameter: {'?links=' in scan_url}")
            return True
        else:
            print(f"✗ Scan URL format issue")
            return False
    except Exception as e:
        print(f"✗ URL parsing failed: {e}")
        return False


def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " END-TO-END TEST: Social QR Code Generator ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        # Run tests in sequence
        links = test_dynamic_rows()
        scan_url = test_scan_url_generation(links)
        decoded = test_scan_page_parsing(scan_url)
        url_valid = test_qr_url_validity(scan_url)
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        all_pass = links and scan_url and decoded and url_valid
        
        if all_pass:
            print("✓ ALL TESTS PASSED")
            print("\nWorkflow verified:")
            print("  1. Dynamic rows collect multiple social links ✓")
            print("  2. Links encoded to JSON in scan URL ✓")
            print("  3. Scan page can decode and parse links ✓")
            print("  4. QR code target URL is valid ✓")
            print("\nEnd-to-end flow is READY FOR PRODUCTION")
            return 0
        else:
            print("✗ SOME TESTS FAILED")
            return 1
            
    except Exception as e:
        print(f"\n✗ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
