#!/usr/bin/env python3
"""
Fetch OBIS nodes and institutes from the OBIS API and save as JSON files.
"""
import json
import urllib.request
from pathlib import Path

def fetch_obis_nodes():
    """Fetch all OBIS nodes from API."""
    url = "https://api.obis.org/node"
    print(f"Fetching OBIS nodes from {url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching nodes: {e}")
        return None


def fetch_obis_institutes():
    """Fetch all OBIS institutes from API."""
    url = "https://api.obis.org/institute"
    print(f"Fetching OBIS institutes from {url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching institutes: {e}")
        return None


def save_nodes(nodes_data):
    """Save nodes data to JSON file."""
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "obis-nodes.json"
    
    with open(output_file, 'w') as f:
        json.dump(nodes_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(nodes_data.get('results', []))} nodes to {output_file}")


def save_institutes(institutes_data):
    """Save institutes data to JSON file."""
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "obis-institutes.json"
    
    with open(output_file, 'w') as f:
        json.dump(institutes_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(institutes_data.get('results', []))} institutes to {output_file}")


def main():
    """Main function to fetch and save OBIS data."""
    print("OBIS Data Fetcher")
    print("=" * 50)
    
    # Fetch nodes
    nodes = fetch_obis_nodes()
    if nodes:
        save_nodes(nodes)
    else:
        print("Warning: Could not fetch nodes data")
    
    print()
    
    # Fetch institutes
    institutes = fetch_obis_institutes()
    if institutes:
        save_institutes(institutes)
    else:
        print("Warning: Could not fetch institutes data")
    
    print()
    print("Done! You can now build the site with: npm run build")


if __name__ == "__main__":
    main()
