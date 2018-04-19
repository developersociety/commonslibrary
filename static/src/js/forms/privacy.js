const owner_group = document.querySelector('#id_organisation');
const public_field = document.querySelector('#id_is_public');
const privacy_field = document.querySelector('#div_id_privacy');
const privacy_options = privacy_field.querySelectorAll('input');

let selected_owner = undefined;

owner_group.onchange=() => {
    let owner_privacy_option;

    // get selected org id
    selected_owner = owner_group.options[owner_group.selectedIndex].value

    // if org is selected hide from privacy
    if (selected_owner) {
        remove_class('#div_id_privacy .multiselect-option', 'sr__input');
        owner_privacy_option = get_checkbox(selected_owner);
        owner_privacy_option.classList.add('sr__input');
    } else {
        remove_class('#div_id_privacy .multiselect-option', 'sr__input');
    }
}

public_field.onchange=() => {
    const is_public = public_field.checked;

    // show field only if a user is a member of more than one group
    if (!is_public && privacy_options.length > 1) {
        privacy_field.classList.remove('sr__input');
    }

    [...privacy_options].map(option => {
        option.checked = !is_public;
    })
}

// remove class of given query selector
function remove_class(query, css_class) {
    [...document.querySelectorAll(query)].map(element => {
        element.classList.remove(css_class);
    })
}

function get_checkbox(value) {
    let checkbox;

    [...document.querySelectorAll('#div_id_privacy .multiselect-option input')].map(element => {
        if (element.value == value) {
            checkbox = element.parentNode;
        }
    })

    return checkbox;
}
