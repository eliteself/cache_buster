#!/usr/bin/env python3
"""
Cache Buster for eliteself.tech
Automatically generates cache-busting hashes for static files
"""

import hashlib
import os
import re
from pathlib import Path

def get_file_hash(file_path):
    """Generate SHA-256 hash of file content"""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:8]

# change name if need of your website folders where saved .css and .js files
def update_html_files():
    """Update HTML files with cache-busting hashes"""
    static_dir = Path("static")
    templates_dir = Path("templates")
    
    # Get hashes for static files
    file_hashes = {}
    for file_path in static_dir.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(static_dir)
            file_hashes[str(relative_path)] = get_file_hash(file_path)
    
    # Update HTML files
    for html_file in templates_dir.glob("*.html"):
        print(f"Processing {html_file}...")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # file path of you website
        # Update CSS files
        content = re.sub(
            r'href="/static/([^"]+\.css)(?:\?v=[^"]*)?"',
            lambda m: f'href="/static/{m.group(1)}?v={file_hashes.get(m.group(1), "1.0")}"',
            content
        )
        
        # file path of you website
        # Update JS files
        content = re.sub(
            r'src="/static/([^"]+\.js)(?:\?v=[^"]*)?"',
            lambda m: f'src="/static/{m.group(1)}?v={file_hashes.get(m.group(1), "1.0")}"',
            content
        )
        
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {html_file}")

def main():
    """Main function"""
    print("🔄 Starting cache busting process...")
    update_html_files()
    print("✅ Cache busting complete!")

if __name__ == "__main__":
    main() 
