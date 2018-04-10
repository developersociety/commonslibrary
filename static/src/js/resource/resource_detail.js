import Sticky from 'sticky-js';

new Sticky('#resource_sidebar', {
    'stickyFor': 1260
});

const csrf = document.querySelector('[name="csrfmiddlewaretoken"]').value;
const resource = document.querySelector('.resource-holder').dataset.resource;
const actionButtons = document.querySelectorAll('.js-resource-action');
const accordions = document.querySelectorAll('.mj_accordion');

function resourceAction(action, button) {
    const requestUrl = '/api/v1/resources/' + resource + '/' + action +'/';
    const allButtonsOfType = document.querySelectorAll('[data-type=' + action + ']');

    fetch(requestUrl, {
        method: 'put',
        credentials: 'include',
        headers: {
            "X-CSRFToken": csrf
        }
    }).then(response => {
        if (response.ok) {
            const prevStatus = button.classList.contains('true');
            const newStatus = !prevStatus;

            [...allButtonsOfType].map(button => {
                button.classList.replace(prevStatus.toString(), newStatus.toString());

                let count = button.querySelector('.js-count');
                let oldCount = parseInt(count.textContent);

                count.textContent = newStatus == true ? oldCount + 1 : oldCount - 1;
            })
        }
    })
}

[...actionButtons].map(button => {
    button.addEventListener('click', e => {
        e.preventDefault();

        const button = e.target.parentElement;
        const type = button.dataset.type;

        resourceAction(type, button);
    })
});

[...accordions].map(accordion => {
    const accordionPanels = accordion.children;
    const accordionToggles = accordion.querySelectorAll('.mj_accordion_item');

    [...accordionToggles].map(toggle => {
        toggle.addEventListener('click', e => {
            const panel = e.target.parentElement;
            const panelClass = panel.classList

            panelClass.contains('active') ? panelClass.remove('active') : panelClass.add('active');
        })
    });
});



