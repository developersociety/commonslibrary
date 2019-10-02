const category_toggles = document.querySelectorAll('.category_toggle');
const category_details = document.querySelectorAll('.resources-holder');

category_toggles.forEach((category) => {
    category.onclick = (event) => {
        event.preventDefault();

        category_details.forEach((detail_panel) => {
            detail_panel.classList.add('hidden');
        });

        const target = category.dataset.target;
        const target_element = document.querySelector(
            `.resources-holder[data-category="${target}"]`
        );

        target_element.classList.remove('hidden');
    };
});
