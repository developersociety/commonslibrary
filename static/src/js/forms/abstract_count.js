window.onload = function() {
    const textArea = document.getElementById('id_abstract');
    const characterCounter = document.querySelector('.char-count');

    // Set current length for textarea
    characterCounter.textContent = textArea.textContent.length;

    const countCharacters = () => {
        const numOfEnteredChars = textArea.value.length;
        const counter = numOfEnteredChars;
        characterCounter.textContent = counter;
    };

    // Attach event for textarea
    textArea.addEventListener('input', countCharacters);
};
