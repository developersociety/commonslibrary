const profile_dropdown = document.querySelector('#profile_dropdown');
const profile_dropdown_trigger = document.querySelector('#profile_dropdown_toggle');

let profile_dropdown_open = false;
let didScroll = false;
let lastScrollTop = 0;
const scrollDelta = 5;

function hasScrolled() {
    const scrollTop = window.scrollY;
    const navbarHeight = document.querySelector('.page-navigation__home').offsetHeight;
    const pageHead = document.querySelector('.page-head');

    if (Math.abs(lastScrollTop - scrollTop) <= scrollDelta) {
        return;
    }

    // If they scrolled down and are past the navbar, add class .nav-up.
    // This is necessary so you never see what is "behind" the navbar.
    if (scrollTop > lastScrollTop && scrollTop > navbarHeight) {
        // Scroll Down
        pageHead.classList.remove('shown');
        pageHead.classList.add('not-shown');

        if (profile_dropdown !== null && profile_dropdown.classList.contains('shown-true')) {
            profile_dropdown_trigger.click();
        }
    } else {
        // Scroll Up
        if (scrollTop + window.outerHeight < document.documentElement.scrollHeight) {
            pageHead.classList.remove('not-shown');
            pageHead.classList.add('shown');
        }
    }

    lastScrollTop = scrollTop;
}
window.addEventListener('scroll', (e) => {
    didScroll = true;
});

window.setInterval(() => {
    if (didScroll && window.outerWidth <= 1060) {
        hasScrolled();
        didScroll = false;
    }
});

if (profile_dropdown !== null) {
    profile_dropdown_trigger.onclick = () => {
        profile_dropdown.classList.remove(`shown-${profile_dropdown_open}`);
        profile_dropdown_open = !profile_dropdown_open;
        profile_dropdown.classList.add(`shown-${profile_dropdown_open}`);
    };
}
