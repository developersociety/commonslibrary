const category_toggles = document.querySelectorAll('.category_toggle');
const category_details = document.querySelectorAll('.resources-holder');

category_toggles.forEach((category) => {
    category.onclick = (event) => {
        event.preventDefault();

        const category_element = category.closest('.category-grid__item');
        const height_offset = category_element.offsetTop + category_element.offsetHeight;

        category_details.forEach((detail_panel) => {
            detail_panel.classList.add('hidden');
        });

        category_toggles.forEach((category_toggle) => {
            category_toggle.closest('.category-grid__item').classList.remove('active');
        });

        // Add active to the category
        category_element.closest('.category-grid__item').classList.add('active');

        const target = category.dataset.target;
        const target_element = document.querySelector(
            `.resources-holder[data-category="${target}"]`
        );

        target_element.style.top = `${height_offset}px`;
        target_element.classList.remove('hidden');
    };
});
