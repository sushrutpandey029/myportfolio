// Projects Page JavaScript
// Handles scroll animations and project filtering

// Scroll Reveal Animation
document.addEventListener('DOMContentLoaded', () => {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.scroll-reveal').forEach(el => {
        observer.observe(el);
    });

    // Smooth scroll for category links
    document.querySelectorAll('.category-pill').forEach(link => {
        link.addEventListener('click', (e) => {
            if (link.getAttribute('href') && link.getAttribute('href').includes('category=')) {
                // Should only be needed if using backend routing, but buttons mostly use onclick="filterProjects"
                // The backend pagination links might trigger this.
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });
});

// Client-side filtering function for projects
function filterProjects(category) {
    const projectItems = document.querySelectorAll('.project-item');
    const filterButtons = document.querySelectorAll('.category-filter');

    // Update active state on filter buttons
    filterButtons.forEach(btn => {
        if (btn.dataset.category === category) {
            btn.classList.add('active', 'text-white');
            btn.classList.remove('text-text-secondary');
        } else {
            btn.classList.remove('active', 'text-white');
            btn.classList.add('text-text-secondary');
        }
    });

    // Filter project items with smooth animation
    let visibleIndex = 0;
    projectItems.forEach((item) => {
        const itemCategory = item.dataset.category;
        const matches = (category === 'All' || itemCategory === category);

        if (matches) {
            item.style.display = 'block';
            // Simple delay calc only for visible items
            setTimeout(() => {
                item.style.opacity = '0';
                item.style.transform = 'scale(0.9) translateY(20px)';

                setTimeout(() => {
                    item.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
                    item.style.opacity = '1';
                    item.style.transform = 'scale(1) translateY(0)';
                }, 50);
            }, visibleIndex * 50); // faster delay
            visibleIndex++;
        } else {
            item.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
            item.style.opacity = '0';
            item.style.transform = 'scale(0.95) translateY(10px)';
            setTimeout(() => {
                item.style.display = 'none';
            }, 400);
        }
    });

    // Smooth scroll to projects grid (if grid exists)
    const grid = document.querySelector('.grid');
    if (grid) {
        window.scrollTo({ top: grid.offsetTop - 100, behavior: 'smooth' });
    }
}
