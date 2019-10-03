import Sticky from 'sticky-js';

new Sticky('#resource_sidebar', {
    stickyFor: 1060
});

const csrf = document.querySelector('[name="csrfmiddlewaretoken"]').value;
const resource = document.querySelector('.resource-holder').dataset.resource;
const actionButtons = document.querySelectorAll('.js-resource-action');
const accordions = document.querySelectorAll('.mj_accordion');

function resourceAction(action, button) {
    const requestUrl = `/api/v1/resources/${resource}/${action}/`;
    const allButtonsOfType = document.querySelectorAll(`[data-type=${action}]`);

    fetch(requestUrl, {
        method: 'put',
        credentials: 'include',
        headers: {
            'X-CSRFToken': csrf
        }
    }).then((response) => {
        if (response.ok) {
            const prevStatus = button.classList.contains('true');
            const newStatus = !prevStatus;

            [...allButtonsOfType].map((button_instance) => {
                button_instance.classList.replace(prevStatus.toString(), newStatus.toString());

                const count = button_instance.querySelector('.js-count');
                const oldCount = parseInt(count.textContent, 10);

                count.textContent = newStatus === true ? oldCount + 1 : oldCount - 1;
            });
        }
    });
}

[...actionButtons].map((button) => {
    button.addEventListener('click', (e) => {
        e.preventDefault();

        const button_element = e.target.parentElement;
        const type = button_element.dataset.type;

        resourceAction(type, button_element);
    });
});

[...accordions].map((accordion) => {
    const accordionToggles = accordion.querySelectorAll('.mj_accordion_item');

    [...accordionToggles].map((toggle) => {
        toggle.addEventListener('click', (e) => {
            const panel = e.target.parentElement;
            const panelClass = panel.classList;

            if (panelClass.contains('active')) {
                panelClass.remove('active');
            } else {
                panelClass.add('active');
            }
        });
    });
});
