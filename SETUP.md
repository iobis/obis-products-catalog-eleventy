# OBIS Products Catalog - Setup Guide

## What's included

This proof of concept includes:
- Complete Eleventy static site generator setup
- Python harvest script for fetching metadata from DOIs
- Sample product data (4 example products)
- Client-side search and filtering
- OBIS node and institution grouping pages
- GitHub Actions workflow for automated deployment
- Responsive design using Pico.css

## Local Setup

1. **Extract the archive**
   ```bash
   tar -xzf obis-products-catalog.tar.gz
   cd obis-products-catalog
   ```

2. **Install dependencies**
   ```bash
   npm install
   pip install pyyaml
   ```

3. **View the sample site**
   ```bash
   npm run serve
   ```
   Open http://localhost:8080 in your browser

## Harvesting Real Data

When you have network access, run the harvest script:

```bash
python scripts/harvest.py
```

This will:
- Read DOIs from `data/whitelist.txt`
- Fetch metadata from Zenodo/DataCite APIs
- Apply OBIS associations from `data/mappings.yaml`
- Save JSON-LD files to `data/products/`

## GitHub Setup

1. **Create a new GitHub repository**

2. **Initialize and push**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: GitHub Actions
   - The workflow will automatically deploy on push

4. **Your site will be live at:**
   `https://YOUR-USERNAME.github.io/YOUR-REPO/`

## Adding Products

### Method 1: Add to whitelist
1. Edit `data/whitelist.txt`
2. Add DOI (one per line)
3. Run `python scripts/harvest.py`
4. Commit and push

### Method 2: Direct PR to mappings
1. Fork the repository
2. Edit `data/mappings.yaml` in GitHub web interface
3. Add OBIS node/institution associations
4. Submit pull request

Example mapping:
```yaml
products:
  - doi: 10.5281/zenodo.12345
    obis_nodes:
      - id: obis-usa
        name: OBIS-USA
        url: https://obis.org/node/usa
    institutions:
      - id: example-inst
        name: Example Institution
        role: data_provider
```

## File Structure

```
obis-products-catalog/
├── .eleventy.js              # Eleventy configuration
├── package.json              # Node dependencies
├── data/
│   ├── whitelist.txt         # List of DOIs to harvest
│   ├── mappings.yaml         # OBIS associations
│   └── products/             # Generated JSON-LD files
├── scripts/
│   └── harvest.py            # Metadata harvester
├── _includes/
│   ├── base.njk              # Base layout
│   ├── product.njk           # Product page template
│   ├── node-page.njk         # Node page template
│   └── institution-page.njk  # Institution page template
├── css/
│   └── custom.css            # Custom styles
├── js/
│   └── filter.js             # Client-side filtering
├── index.njk                 # Homepage with search
├── nodes.njk                 # Nodes index page
├── institutions.njk          # Institutions index page
└── .github/
    └── workflows/
        └── deploy.yml        # Auto-deployment workflow
```

## Features

- ✅ Static site generation (Eleventy)
- ✅ Automated metadata harvesting from Zenodo/DataCite
- ✅ Schema.org JSON-LD embedded in every page
- ✅ Client-side search and filtering
- ✅ Filter by OBIS node or institution
- ✅ Grouped views (by node, by institution)
- ✅ Responsive design (Pico.css)
- ✅ GitHub Actions auto-deployment
- ✅ Version controlled (git)
- ✅ Zero database, zero backend

## Next Steps

1. Test locally with sample data
2. Add real OBIS node/institution mappings
3. Run harvest script to fetch real metadata
4. Deploy to GitHub Pages
5. Share with OBIS community for feedback

## Customization

- **Branding**: Edit `css/custom.css` (change `--obis-blue` color)
- **Templates**: Modify files in `_includes/`
- **Search**: Customize `js/filter.js`
- **Metadata**: Adjust `scripts/harvest.py` for additional fields

## Troubleshooting

**Site won't build?**
- Check `npm install` ran successfully
- Verify JSON-LD files in `data/products/` are valid JSON

**Harvest script fails?**
- Check network connectivity
- Verify DOI format in whitelist
- Some DOIs may not be in Zenodo (will try DataCite)

**Filters not working?**
- Ensure products have node/institution data
- Check browser console for JavaScript errors
