// Home page specific JavaScript

// Add any interactive functionality here
document.addEventListener('DOMContentLoaded', function () {
    // Add scroll effect to navbar
    const navbar = document.querySelector('header');

    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
});

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function () {
    const menuButton = document.querySelector('.lg\\:hidden');
    const mobileMenu = document.querySelector('.mobile-menu');

    if (menuButton && mobileMenu) {
        menuButton.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });
    }
});