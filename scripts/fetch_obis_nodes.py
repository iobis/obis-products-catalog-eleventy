#!/usr/bin/env python3
"""
Fetch OBIS nodes and institutes from the OBIS API.
"""
import json
import urllib.request
from pathlib import Path


def fetch_obis_nodes():
    """Fetch all OBIS nodes from API."""
    url = "https://api.obis.org/node"
    print(f"Fetching OBIS nodes from {url}")
    
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
        print(f"Error fetching nodes: {e}")
        return None


def save_nodes(nodes_data):
    """Save nodes data to JSON file."""
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "obis-nodes.json"
    
    with open(output_file, 'w') as f:
        json.dump(nodes_data, f, indent=2, ensure_ascii=False)
    
    num_nodes = len(nodes_data.get('results', [])) if isinstance(nodes_data, dict) else len(nodes_data)
    print(f"Saved {num_nodes} nodes to {output_file}")


def main():
    nodes = fetch_obis_nodes()
    if nodes:
        save_nodes(nodes)
        print("\nDone! You can now use this data in your Eleventy build.")
    else:
        print("Failed to fetch OBIS nodes data")


if __name__ == "__main__":
    main()