import Taggle from 'taggle';
import $ from 'jquery';
import 'jquery-ui/ui/widgets/autocomplete';

const tag_fields = document.querySelectorAll('.tag-group');

[...tag_fields].map(field => {
    const select = field.querySelector('select');
    const options = [];
    const selected = [];

    [...select.options].map(option => {
        options.push(option.text);

        // if previously selected push to list
        if (option.selected) {
            selected.push(option.text)
        }
    })

    const taggleField = new Taggle(field.querySelector('.tag-select'), {
        tags: selected,
        allowedTags: options,
        placeholder: 'type to search for tags',
        onTagAdd: function(event, tag) {
            [...select.options].map(option => {
                if (option.text.toLowerCase() == tag) {
                    option.selected = true;
                }
            })
        },
        onTagRemove: function(event, tag) {
            [...select.options].map(option => {
                if (option.text.toLowerCase() == tag) {
                    option.selected = false;
                }
            })
        }
    });

    var container = taggleField.getContainer();
    var input = taggleField.getInput();

    $(input).autocomplete({
        source: options, // See jQuery UI documentaton for options
        appendTo: container,
        position: { at: "left bottom", of: container },
        select: function(event, data) {
            event.preventDefault();
            //Add the tag if user clicks
            if (event.which === 1) {
                taggleField.add(data.item.value);
            }
        }
    })
})
