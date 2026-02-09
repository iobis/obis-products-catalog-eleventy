// Client-side search and filter for OBIS Products Catalog

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Pagefind search
    if (document.getElementById('pagefind-search')) {
        new PagefindUI({ 
            element: "#pagefind-search",
            showSubResults: true,
            showImages: false,
            excerptLength: 30
        });
    }
    
    const productCards = document.querySelectorAll('.product-card');
    const nodeFilters = document.querySelectorAll('.node-filter');
    const institutionFilters = document.querySelectorAll('.institution-filter');
    const resultsCount = document.getElementById('results-count');
    const categoryFilters = document.querySelectorAll('.category-filter');

    if (!productCards.length) return;
    
    const totalProducts = productCards.length;
    
    // Filter state
    const filterState = {
        nodes: {
            include: [],
            exclude: []
        },
        institutions: {
            include: [],
            exclude: []
        },
        categories: {
            include: [],
            exclude: []
        }
    };
    
    // Filter function
    function applyFilters() {
        let visibleCount = 0;
        
        productCards.forEach(card => {
            let show = true;
            
            // Node filters
            const cardNodes = (card.dataset.nodes || '').split(',').filter(n => n);
            
            // Include filters (OR logic)
            if (filterState.nodes.include.length > 0) {
                const hasIncludedNode = filterState.nodes.include.some(nodeId => 
                    cardNodes.includes(nodeId)
                );
                if (!hasIncludedNode) {
                    show = false;
                }
            }
            
            // Exclude filters
            if (filterState.nodes.exclude.length > 0) {
                const hasExcludedNode = filterState.nodes.exclude.some(nodeId => 
                    cardNodes.includes(nodeId)
                );
                if (hasExcludedNode) {
                    show = false;
                }
            }
            
            // Institution filters
            const cardInstitutions = (card.dataset.institutions || '').split(',').filter(i => i);
            
            // Include filters (OR logic)
            if (filterState.institutions.include.length > 0) {
                const hasIncludedInst = filterState.institutions.include.some(instId => 
                    cardInstitutions.includes(instId)
                );
                if (!hasIncludedInst) {
                    show = false;
                }
            }
            
            // Exclude filters
            if (filterState.institutions.exclude.length > 0) {
                const hasExcludedInst = filterState.institutions.exclude.some(instId => 
                    cardInstitutions.includes(instId)
                );
                if (hasExcludedInst) {
                    show = false;
                }
            }
            
            // Category filters
            const cardCategory = card.dataset.category || '';
            
            if (filterState.categories.include.length > 0) {
                if (!filterState.categories.include.includes(cardCategory)) {
                    show = false;
                }
            }
            
            if (filterState.categories.exclude.length > 0) {
                if (filterState.categories.exclude.includes(cardCategory)) {
                    show = false;
                }
            }

            // Apply visibility
            if (show) {
                card.classList.remove('hidden');
                visibleCount++;
            } else {
                card.classList.add('hidden');
            }
        });
        
        // Update results count
        if (resultsCount) {
            resultsCount.textContent = `Showing ${visibleCount} of ${totalProducts} products`;
        }
    }
    
    // Node filter handlers
    nodeFilters.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const nodeId = this.value;
            const filterType = this.dataset.filterType || 'include';
            
            if (this.checked) {
                filterState.nodes[filterType].push(nodeId);
            } else {
                const index = filterState.nodes[filterType].indexOf(nodeId);
                if (index > -1) {
                    filterState.nodes[filterType].splice(index, 1);
                }
            }
            
            applyFilters();
        });
    });
    
    // Institution filter handlers
    institutionFilters.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const instId = this.value;
            const filterType = this.dataset.filterType || 'include';
            
            if (this.checked) {
                filterState.institutions[filterType].push(instId);
            } else {
                const index = filterState.institutions[filterType].indexOf(instId);
                if (index > -1) {
                    filterState.institutions[filterType].splice(index, 1);
                }
            }
            
            applyFilters();
        });
    });

    // Category filter handlers
    categoryFilters.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const category = this.value;
            const filterType = this.dataset.filterType || 'include';
            
            if (this.checked) {
                filterState.categories[filterType].push(category);
            } else {
                const index = filterState.categories[filterType].indexOf(category);
                if (index > -1) {
                    filterState.categories[filterType].splice(index, 1);
                }
            }
            
            applyFilters();
        });
    });
    
});

// Client-side search and filter for OBIS Products Catalog

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Pagefind search
    if (document.getElementById('pagefind-search')) {
        new PagefindUI({ 
            element: "#pagefind-search",
            showSubResults: true,
            showImages: false,
            excerptLength: 30
        });
    }
    
    const productCards = document.querySelectorAll('.product-card');
    const nodeFilters = document.querySelectorAll('.node-filter');
    const institutionFilters = document.querySelectorAll('.institution-filter');
    const resultsCount = document.getElementById('results-count');
    const categoryFilters = document.querySelectorAll('.category-filter');

    if (!productCards.length) return;
    
    const totalProducts = productCards.length;
    
    // Filter state
    const filterState = {
        nodes: {
            include: [],
            exclude: []
        },
        institutions: {
            include: [],
            exclude: []
        },
        categories: {
            include: [],
            exclude: []
        }
    };
    
    // DOI search
    const doiSearchInput = document.getElementById('doi-search');
    const doiResults = document.getElementById('doi-results');
    
    if (doiSearchInput) {
        doiSearchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.trim().toLowerCase();
            
            if (!searchTerm) {
                // Reset - show all products based on existing filters
                productCards.forEach(card => {
                    if (!card.classList.contains('hidden')) {
                        card.style.display = '';
                    }
                });
                if (doiResults) doiResults.innerHTML = '';
                return;
            }
            
            let matchCount = 0;
            productCards.forEach(card => {
                // Look for DOI in the card
                const doiLink = card.querySelector('a[href*="doi.org"]');
                if (doiLink && doiLink.href.toLowerCase().includes(searchTerm)) {
                    card.style.display = '';
                    matchCount++;
                } else {
                    card.style.display = 'none';
                }
            });
            
            if (doiResults) {
                doiResults.innerHTML = `<small>${matchCount} product(s) matching "${searchTerm}"</small>`;
            }
        });
    }
    
}); // End of DOMContentLoaded