const { DateTime } = require("luxon");

module.exports = function(eleventyConfig) {
  // Pass through static assets
  eleventyConfig.addPassthroughCopy("css");
  eleventyConfig.addPassthroughCopy("js");
  
  // Date filter
  eleventyConfig.addFilter("readableDate", dateObj => {
    return DateTime.fromJSDate(new Date(dateObj)).toFormat("dd LLL yyyy");
  });

  // Create collections
  eleventyConfig.addCollection("products", function(collectionApi) {
    const fs = require('fs');
    const path = require('path');
    const productsDir = path.join(__dirname, 'data/products');
    
    // Check if directory exists
    if (!fs.existsSync(productsDir)) {
      return [];
    }
    
    const products = [];
    const files = fs.readdirSync(productsDir);
    
    files.forEach(file => {
      if (file.endsWith('.json')) {
        const filePath = path.join(productsDir, file);
        const content = fs.readFileSync(filePath, 'utf8');
        const product = JSON.parse(content);
        product.url = `/products/${product.zenodo_id}/`;
        products.push(product);
      }
    });
    
    // Sort by date, newest first
    return products.sort((a, b) => {
      const dateA = new Date(a.publication_date || 0);
      const dateB = new Date(b.publication_date || 0);
      return dateB - dateA;
    });
  });

  // Group products by institution
  eleventyConfig.addCollection("byInstitution", function(collectionApi) {
    const fs = require('fs');
    const path = require('path');
    const productsDir = path.join(__dirname, 'data/products');
    const byInst = {};
    
    if (!fs.existsSync(productsDir)) {
      return [];
    }
    
    const files = fs.readdirSync(productsDir);
    
    files.forEach(file => {
      if (file.endsWith('.json')) {
        const filePath = path.join(productsDir, file);
        const content = fs.readFileSync(filePath, 'utf8');
        const product = JSON.parse(content);
        product.url = `/products/${product.zenodo_id}/`;
        
        if (product.institutions) {
          product.institutions.forEach(inst => {
            if (!byInst[inst.id]) {
              byInst[inst.id] = {
                id: inst.id,
                name: inst.name,
                products: []
              };
            }
            byInst[inst.id].products.push(product);
          });
        }
      }
    });
    
    return Object.values(byInst);
  });

  // Group products by category
  eleventyConfig.addCollection("byCategory", function(collectionApi) {
    const fs = require('fs');
    const path = require('path');
    const productsDir = path.join(__dirname, 'data/products');
    const byCat = {};
    
    if (!fs.existsSync(productsDir)) {
      return [];
    }
    
    const files = fs.readdirSync(productsDir);
    
    files.forEach(file => {
      if (file.endsWith('.json')) {
        const filePath = path.join(productsDir, file);
        const content = fs.readFileSync(filePath, 'utf8');
        const product = JSON.parse(content);
        product.url = `/products/${product.zenodo_id}/`;
        
        const categories = Array.isArray(product.category) ? product.category : [product.category];
        categories.forEach(cat => {
            if (!byCat[cat]) {
                byCat[cat] = { name: cat, products: [] };
            }
            byCat[cat].products.push(product);
        });
      }  // <-- ADD THIS CLOSING BRACE
    });
    
    return Object.values(byCat);
  });

  // Load OBIS nodes data from API
  eleventyConfig.addGlobalData("obisNodes", function() {
    const fs = require('fs');
    const path = require('path');
    const nodesFile = path.join(__dirname, 'data/obis-nodes.json');
    
    if (fs.existsSync(nodesFile)) {
      const data = JSON.parse(fs.readFileSync(nodesFile, 'utf8'));
      // Convert array to lookup by id
      const nodesById = {};
      (data.results || data).forEach(node => {
        nodesById[node.id] = node;
      });
      return nodesById;
    }
    return {};
  });

  // Group products by OBIS node
  eleventyConfig.addCollection("byNode", function(collectionApi) {
    const fs = require('fs');
    const path = require('path');
    const productsDir = path.join(__dirname, 'data/products');
    
    // Load OBIS nodes API data - initialize with ALL nodes
    const nodesFile = path.join(__dirname, 'data/obis-nodes.json');
    const byNode = {};
    
    if (fs.existsSync(nodesFile)) {
      const data = JSON.parse(fs.readFileSync(nodesFile, 'utf8'));
      const nodes = data.results || data;
      
      // Initialize ALL nodes from the API, even if they have no products
      nodes.forEach(node => {
        byNode[node.id] = {
          ...node,  // Include all API data
          products: []  // Start with empty products array
        };
      });
    }
    
    // Now add products to nodes that have them
    if (fs.existsSync(productsDir)) {
      const files = fs.readdirSync(productsDir);
      
      files.forEach(file => {
        if (file.endsWith('.json')) {
          const filePath = path.join(productsDir, file);
          const content = fs.readFileSync(filePath, 'utf8');
          const product = JSON.parse(content);
          product.url = `/products/${product.zenodo_id}/`;
          
          if (product.obis_nodes) {
            product.obis_nodes.forEach(nodeRef => {
              // Add product to the node if it exists in our list
              if (byNode[nodeRef.id]) {
                byNode[nodeRef.id].products.push(product);
              }
            });
          }
        }
      });
    }
    
    return Object.values(byNode);
  });

  return {
    pathPrefix: "/obis-products-catalog-eleventy/",
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes",
      data: "data"
    },
    templateFormats: ["njk", "md", "html", "json"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk"
  };
};
