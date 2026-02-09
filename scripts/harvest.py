#!/usr/bin/env python3
"""
Harvest metadata from DOI providers by scraping schema.org JSON-LD.
"""
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
import urllib.request
import urllib.error
import yaml

def fetch_schema_org_from_page(doi: str) -> Optional[Dict]:
    """Fetch schema.org JSON-LD directly from DOI resolution page."""
    url = f"https://doi.org/{doi}"
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Updated pattern to handle attributes before type
            pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
            matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
            
            # Types to skip (not actual products)
            skip_types = ['BreadcrumbList', 'Organization', 'WebSite', 'WebPage', 'Person']
            
            for match in matches:
                try:
                    data = json.loads(match)
                    context = data.get('@context', '')
                    data_type = data.get('@type', '')
                    
                    # Check for schema.org and skip unwanted types
                    if 'schema.org' in str(context).lower() and data_type not in skip_types:
                        # Normalize description/name
                        if 'description' in data and isinstance(data['description'], list):
                            data['description'] = ' '.join(str(d) for d in data['description'])
                        if 'name' in data and isinstance(data['name'], list):
                            data['name'] = ' '.join(str(n) for d in data['name'])
                        return data
                except json.JSONDecodeError:
                    continue
        
        return None
    except Exception as e:
        print(f"  Error fetching schema.org from {doi}: {e}")
        return None
    
def load_whitelist(filepath: str = "data/whitelist.txt") -> List[str]:
    """Load DOI whitelist from file."""
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


def load_mappings(filepath: str = "data/mappings.yaml") -> List[Dict]:
    """Load OBIS node and institution mappings."""
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('products', []) if data else []
    except FileNotFoundError:
        print(f"Warning: {filepath} not found, continuing without mappings")
        return []


def add_obis_metadata(schema_org: Dict, doi: str, mappings: List[Dict]) -> Dict:
    """Add OBIS-specific metadata from mappings."""
    # Find mapping for this DOI
    mapping = next((m for m in mappings if m.get('doi') == doi), None)
    
    if mapping:
        if mapping.get('obis_nodes'):
            schema_org['obis_nodes'] = mapping['obis_nodes']
        if mapping.get('institutions'):
            schema_org['institutions'] = mapping['institutions']
    
    return schema_org


def save_product(schema_org: Dict, safe_id: str, output_dir: str = "data/products", force: bool = False):
    """Save product metadata as JSON-LD file."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    filepath = Path(output_dir) / f"{safe_id}.json"
    
    # Check if file exists and hasn't changed (unless force=True)
    if not force and filepath.exists():
        with open(filepath, 'r') as f:
            existing = json.load(f)
            # Compare without zenodo_id/publication_date fields
            existing_core = {k: v for k, v in existing.items() if k not in ['zenodo_id', 'publication_date']}
            new_core = {k: v for k, v in schema_org.items() if k not in ['zenodo_id', 'publication_date']}
            
            if existing_core == new_core:
                print(f"  Skipped (unchanged): {filepath}")
                return
    
    with open(filepath, 'w') as f:
        json.dump(schema_org, f, indent=2, ensure_ascii=False)
    
    print(f"  Saved: {filepath}")


def harvest(force=False):
    """Main harvest function."""
    print("OBIS Products Catalog - Metadata Harvester")
    print("=" * 50)
    if force:
        print("FORCE MODE: Re-harvesting all products")
    print()
    
    # Load whitelist and mappings
    dois = load_whitelist()
    mappings = load_mappings()
    
    print(f"Loaded {len(dois)} DOIs from whitelist")
    print(f"Loaded {len(mappings)} mappings")
    print()
    
    # Process each DOI
    for i, doi in enumerate(dois, 1):
        print(f"[{i}/{len(dois)}] Processing {doi}")
        
        # Fetch schema.org from the page
        schema_org = fetch_schema_org_from_page(doi)
        
        if schema_org:
            # Add OBIS metadata
            schema_org = add_obis_metadata(schema_org, doi, mappings)
            
            # Generate safe ID for filename
            safe_id = doi.replace('/', '_').replace('.', '_')
            
            # Add helper fields for our site
            schema_org['zenodo_id'] = safe_id
            schema_org['publication_date'] = schema_org.get('datePublished', '')
            
            # Ensure category field exists - handle arrays
            category = schema_org.get('category') or schema_org.get('@type', 'Other')
            if isinstance(category, list):
                schema_org['category'] = category  # Keep as list
            else:
                schema_org['category'] = [category] if category else ['Other']  # Make it a list
            save_product(schema_org, safe_id, force=force)
            time.sleep(0.5)  # Be nice to servers
        else:
            print(f"  No schema.org found for {doi}")
        
        print()
    
    print("Harvest complete!")


if __name__ == "__main__":
    import sys
    force = '--force' in sys.argv
    harvest(force=force)