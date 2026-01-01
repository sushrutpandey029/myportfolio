// Materials Page JavaScript
// Handles client-side filtering and animations

function filterMaterials(category) {
    const items = document.querySelectorAll('.material-item');
    const buttons = document.querySelectorAll('.category-filter');

    // Update functionality
    buttons.forEach(btn => {
        const checkIcon = btn.querySelector('.check-icon');
        const checkSpan = checkIcon.querySelector('span');

        if (btn.dataset.category === category) {
            checkIcon.classList.add('bg-primary', 'border-primary');
            checkSpan.classList.remove('hidden');
        } else {
            checkIcon.classList.remove('bg-primary', 'border-primary');
            checkSpan.classList.add('hidden');
        }
    });

    // Filter items
    let visibleCount = 0;
    items.forEach((item, index) => {
        const itemCategory = item.dataset.category;

        if (category === 'All' || itemCategory === category) {
            item.style.display = 'flex';
            // Reset animation
            item.style.animation = 'none';
            item.offsetHeight; /* trigger reflow */
            item.style.animation = `fadeInUp 0.5s ease-out forwards ${visibleCount * 0.05}s`;
            visibleCount++;
        } else {
            item.style.display = 'none';
        }
    });

    // Show/Hide No Results Message
    const noResultsMsg = document.getElementById('no-results-message');
    if (noResultsMsg) {
        if (visibleCount === 0) {
            noResultsMsg.classList.remove('hidden');
            noResultsMsg.classList.add('flex');
        } else {
            noResultsMsg.classList.add('hidden');
            noResultsMsg.classList.remove('flex');
        }
    }
}
