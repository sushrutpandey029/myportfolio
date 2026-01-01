/**
 * Services Page Logic
 * This script handles the dynamic functionality of the Services page including:
 * - Fetching Service Data: Retrieves service data from the backend API.
 * - Rendering: Dynamically creates and injects service cards into the grid.
 * - Filtering: Client-side filtering by search term and category.
 * - Pagination: Handles page navigation for larger lists of services.
 * - Animations: Initializes scroll reveal animations for new elements.
 */

document.addEventListener('DOMContentLoaded', function () {
    // State Management
    let allServices = [];
    let filteredServices = [];
    let selectedCategory = 'all';
    const servicesPerPage = 6;
    let currentPage = 1;

    /**
     * Fetches services data from the backend API.
     * Uses the global SERVICES_API_URL variable defined in the HTML.
     */
    async function fetchServices() {
        try {
            // Ensure the URL variable is defined
            if (!window.SERVICES_API_URL) {
                console.error("SERVICES_API_URL is not defined.");
                return;
            }

            const response = await fetch(window.SERVICES_API_URL);
            const data = await response.json();
            allServices = data.services;
            filteredServices = [...allServices];

            // Remove loading spinner
            document.getElementById('loading')?.remove();

            // Initial Render
            renderServices();
            updateResultsCount();
            initScrollReveal();
        } catch (error) {
            console.error('Error fetching services:', error);
            const loading = document.getElementById('loading');
            if (loading) {
                loading.innerHTML = '<p style="color: #ef4444; text-align: center; padding: 60px 20px; font-size: 18px; font-weight: 600;">Failed to load services. Please refresh the page.</p>';
            }
        }
    }

    /**
     * Creates the HTML structure for a single service card.
     * @param {Object} service - The service data object
     * @returns {HTMLElement} - The constructed card element
     */
    function createServiceCard(service) {
        const card = document.createElement('div');
        card.className = 'scroll-reveal';

        const imageUrl = service.image_url ? '/static/' + service.image_url : 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&q=80';

        card.innerHTML = `
        <article class="service-card">
            <!-- Image Area -->
            <div class="service-image-wrapper">
                <img src="${imageUrl}" alt="${service.title}" class="service-image">
                
                <!-- Badges (Category & Premium) -->
                <div class="service-badges">
                    <span class="badge badge-category">${service.category}</span>
                    <span class="badge badge-premium">
                        <span class="material-symbols-outlined" style="font-size: 12px;">verified</span>
                        Premium
                    </span>
                </div>
            </div>

            <!-- Content Area -->
            <div class="service-content">
                <h3 class="service-title">${service.title}</h3>
                
                <p class="service-description">
                    ${service.description.substring(0, 130)}${service.description.length > 130 ? '...' : ''}
                </p>

                <!-- Meta Info (Delivery & Revisions) -->
                <div class="service-meta">
                    <div class="meta-item">
                        <span class="material-symbols-outlined">schedule</span>
                        <span>3-5 Days</span>
                    </div>
                    <div class="meta-item">
                        <span class="material-symbols-outlined">cached</span>
                        <span>Revisions</span>
                    </div>
                </div>

                <!-- Footer (Price & CTA) -->
                <div class="service-footer">
                    ${service.price ? `
                        <div class="service-price">
                            <span class="price-label">Starting from</span>
                            <span class="price-value">₹${service.price.toLocaleString()}</span>
                        </div>
                    ` : `
                        <div class="service-price">
                            <span class="price-contact">Contact for Price</span>
                        </div>
                    `}
                    
                    <a href="/services/service/${service.id}" class="btn-view">
                        <span>View</span>
                        <span class="material-symbols-outlined" style="font-size: 18px;">arrow_forward</span>
                    </a>
                </div>
            </div>
        </article>
    `;

        return card;
    }

    /**
     * Renders the grid of service cards based on filtering and pagination.
     */
    function renderServices() {
        const grid = document.getElementById('services-grid');
        const empty = document.getElementById('empty-state');

        // Pagination Logic
        const startIdx = (currentPage - 1) * servicesPerPage;
        const endIdx = startIdx + servicesPerPage;
        const toShow = filteredServices.slice(startIdx, endIdx);

        grid.innerHTML = '';

        // Handle Empty Results
        if (toShow.length === 0) {
            empty.style.display = 'block';
            return;
        }

        empty.style.display = 'none';

        // Append Cards
        toShow.forEach(service => {
            grid.appendChild(createServiceCard(service));
        });

        // Initialize animations and pagination controls
        initScrollReveal();
        renderPagination();
    }

    /**
     * Global function to select a category filter.
     * Exposed to window for onclick handler in HTML.
     */
    window.selectCategory = function (btn, category) {
        document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        selectedCategory = category;
        filterServices();
    };

    /**
     * Filters services based on search input and selected category.
     * Resets pagination to page 1 on filter change.
     */
    function filterServices() {
        const searchTerm = document.getElementById('search-input').value.toLowerCase();

        filteredServices = allServices.filter(service => {
            const matchSearch = !searchTerm ||
                service.title.toLowerCase().includes(searchTerm) ||
                service.description.toLowerCase().includes(searchTerm);

            const matchCategory = selectedCategory === 'all' ||
                service.category.toLowerCase() === selectedCategory;

            return matchSearch && matchCategory;
        });

        currentPage = 1;
        renderServices();
        updateResultsCount();
    }

    /**
     * Updates the text showing the total number of found services.
     */
    function updateResultsCount() {
        const count = filteredServices.length;
        document.getElementById('results-count').textContent =
            `${count} service${count !== 1 ? 's' : ''} available`;
    }

    /**
     * Renders the pagination buttons.
     */
    function renderPagination() {
        const totalPages = Math.ceil(filteredServices.length / servicesPerPage);
        const container = document.getElementById('pagination');

        if (totalPages <= 1) {
            container.innerHTML = '';
            return;
        }

        let html = '';

        // Previous Button
        html += `
        <button class="page-btn" onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
            <span class="material-symbols-outlined">chevron_left</span>
        </button>
    `;

        // Page Numbers
        for (let i = 1; i <= totalPages; i++) {
            html += `
            <button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="changePage(${i})">
                ${i}
            </button>
        `;
        }

        // Next Button
        html += `
        <button class="page-btn" onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
            <span class="material-symbols-outlined">chevron_right</span>
        </button>
    `;

        container.innerHTML = html;
    }

    /**
     * Global function to handle page changes.
     * Exposed to window for onclick handler.
     */
    window.changePage = function (page) {
        const totalPages = Math.ceil(filteredServices.length / servicesPerPage);
        if (page < 1 || page > totalPages) return;
        currentPage = page;
        renderServices();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    /**
     * Initializes the Intersection Observer for scroll reveal animations.
     */
    function initScrollReveal() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el));
    }

    // Event Listeners for Search Input
    document.getElementById('search-input').addEventListener('input', filterServices);

    // Event Listener for "Show All" button in empty state
    document.getElementById('show-all-btn')?.addEventListener('click', function () {
        document.getElementById('search-input').value = '';
        selectedCategory = 'all';
        document.querySelectorAll('.category-pill').forEach(p => {
            p.classList.remove('active');
            if (p.dataset.category === 'all') p.classList.add('active');
        });
        filteredServices = [...allServices];
        currentPage = 1;
        renderServices();
        updateResultsCount();
    });

    // Initialize Page
    fetchServices();
    initScrollReveal();
});
