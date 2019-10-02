const category_toggles = document.querySelectorAll('.category_toggle');

category_toggles.forEach((category) => {
    category.onclick = (event) => {
        event.preventDefault();

        const target = category.dataset.target;
        const target_element = document.querySelector(
            `.resources-holder[data-category="${target}"]`
        );

        target_element.classList.toggle('hidden');
    };
});
