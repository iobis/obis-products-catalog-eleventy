# OBIS Products Catalog

Static catalog for OBIS-related products harvested from Zenodo and other repositories.

## Quick Start

```bash
# Install dependencies
npm install
pip install pyyaml

# Harvest metadata from DOIs
python scripts/harvest.py

# Build site
npm run build

# Or serve locally
npm run serve
```

## File Structure

- `data/whitelist.txt` - List of DOIs to include
- `data/mappings.yaml` - OBIS node and institution associations
- `data/products/` - Generated JSON-LD metadata files
- `scripts/harvest.py` - Metadata harvester
- `_site/` - Generated static site

## Adding Products

1. Add DOI to `data/whitelist.txt`
2. Optionally add OBIS associations in `data/mappings.yaml`
3. Run `python scripts/harvest.py`
4. Commit and push to deploy

## Deployment

GitHub Actions automatically builds and deploys to GitHub Pages on push to main.
