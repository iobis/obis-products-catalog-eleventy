#!/usr/bin/env python3
import json
import re
import urllib.request

doi = "10.6084/m9.figshare.14102825"
url = f"https://doi.org/{doi}"

req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
)

try:
    with urllib.request.urlopen(req) as response:
        # Handle gzip encoding if present
        import gzip
        content = response.read()
        if response.info().get('Content-Encoding') == 'gzip':
            content = gzip.decompress(content)
        html = content.decode('utf-8')
        
    print(f"Fetched {len(html)} bytes")
    
    # Save to file for inspection
    with open('figshare_debug.html', 'w') as f:
        f.write(html)
    print("Saved to figshare_debug.html")
    
    # Try the pattern
    pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
    
    print(f"Found {len(matches)} JSON-LD blocks")
    
    for i, match in enumerate(matches):
        print(f"\n--- Block {i} ---")
        try:
            data = json.loads(match)
            print(f"@type: {data.get('@type')}")
            print(f"@context: {data.get('@context')}")
            print(f"name: {data.get('name', 'N/A')[:50]}...")
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            
except Exception as e:
    print(f"Error: {e}")
