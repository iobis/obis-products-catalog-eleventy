#!/usr/bin/env python3
"""
Fetch OBIS institutes and their OceanExpert details.
"""
import json
import time
import urllib.request
from pathlib import Path


def fetch_obis_institutes():
    """Fetch all OBIS institutes from API."""
    url = "https://api.obis.org/institute"
    print(f"Fetching OBIS institutes from {url}")
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            # Filter out institutes without an id
            institutes = [inst for inst in data.get('results', []) if inst.get('id')]
            return institutes
    except Exception as e:
        print(f"Error fetching institutes: {e}")
        return []


def fetch_oceanexpert_details(institute_id):
    """Fetch detailed info from OceanExpert API."""
    url = f"https://oceanexpert.org/api/v1/institute/{institute_id}.json"
    print(f"  Fetching OceanExpert details for {institute_id}...")
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"  Warning: Could not fetch OceanExpert details for {institute_id}: {e}")
        return None


def main():
    print("OBIS Institutes Fetcher")
    print("=" * 50)
    
    # Fetch OBIS institutes
    obis_institutes = fetch_obis_institutes()
    print(f"\nFound {len(obis_institutes)} institutes with IDs")
    
    # Enrich with OceanExpert data
    enriched = []
    for i, inst in enumerate(obis_institutes, 1):
        print(f"\n[{i}/{len(obis_institutes)}] {inst['name']} (ID: {inst['id']})")
        
        # Get OceanExpert details
        oe_details = fetch_oceanexpert_details(inst['id'])
        
        if oe_details:
            # Merge OBIS and OceanExpert data
            enriched_inst = {
                **inst,  # OBIS data (id, name, country, records)
                'oceanexpert': oe_details  # Full OceanExpert details
            }
            enriched.append(enriched_inst)
        else:
            # Just keep OBIS data if OceanExpert fails
            enriched.append(inst)
        
        # Be nice to APIs
        time.sleep(0.5)
    
    # Save enriched data
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "obis-institutes.json"
    
    with open(output_file, 'w') as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved {len(enriched)} institutes to {output_file}")


if __name__ == "__main__":
    main()