// Videos Page JavaScript
// Handles Carousel and Filtering

let currentSlide = 0;
let autoSlideInterval;
const slideDelay = 5000; // 5 seconds per slide

function showSlide(index) {
    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.carousel-indicator');

    if (!slides.length) return;

    // Wrap around
    if (index >= slides.length) currentSlide = 0;
    if (index < 0) currentSlide = slides.length - 1;
    if (index >= 0 && index < slides.length) currentSlide = index;

    // Hide all slides
    slides.forEach(slide => slide.classList.remove('active'));
    indicators.forEach(ind => ind.classList.remove('active', 'bg-white'));

    // Show current slide
    slides[currentSlide].classList.add('active');
    indicators[currentSlide].classList.add('active', 'bg-white');
}

function nextSlide() {
    showSlide(currentSlide + 1);
    resetAutoSlide();
}

function prevSlide() {
    showSlide(currentSlide - 1);
    resetAutoSlide();
}

function goToSlide(index) {
    showSlide(index);
    resetAutoSlide();
}

function startAutoSlide() {
    autoSlideInterval = setInterval(() => {
        showSlide(currentSlide + 1);
    }, slideDelay);
}

function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
}

// Initialize carousel on page load
document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.carousel-slide');
    if (slides.length > 1) {
        startAutoSlide();
    }
});

// Client-side filtering function
function filterVideos(category) {
    const videoCards = document.querySelectorAll('.video-card');
    const filterButtons = document.querySelectorAll('.category-filter');

    // Update active state on filter buttons
    filterButtons.forEach(btn => {
        if (btn.dataset.category === category) {
            btn.dataset.active = 'true';
            btn.classList.remove('bg-surface-dark', 'ring-white/10');
            btn.classList.add('bg-primary', 'ring-primary', 'text-white');
        } else {
            btn.dataset.active = 'false';
            btn.classList.remove('bg-primary', 'ring-primary');
            btn.classList.add('bg-surface-dark', 'ring-white/10');
        }
    });

    // Filter video cards with smooth animation
    videoCards.forEach((card, index) => {
        const cardCategory = card.dataset.category;

        if (category === 'all' || cardCategory === category) {
            // Show card with staggered animation
            setTimeout(() => {
                card.style.display = 'flex';
                card.style.opacity = '0';
                card.style.transform = 'scale(0.9)';

                setTimeout(() => {
                    card.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
                    card.style.opacity = '1';
                    card.style.transform = 'scale(1)';
                }, 10);
            }, index * 50);
        } else {
            // Hide card
            card.style.transition = 'opacity 0.3s ease-out, transform 0.3s ease-out';
            card.style.opacity = '0';
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.style.display = 'none';
            }, 300);
        }
    });
}
