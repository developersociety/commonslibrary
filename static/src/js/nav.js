let didScroll = false;
let lastScrollTop = 0;
let scrollDelta = 5;

function hasScrolled() {
    let scrollTop = window.scrollY;
    const navbarHeight = document.querySelector('.page-navigation__home').offsetHeight;

    if(Math.abs(lastScrollTop - scrollTop) <= scrollDelta) {
        return
    }

    // If they scrolled down and are past the navbar, add class .nav-up.
    // This is necessary so you never see what is "behind" the navbar.
    if (scrollTop > lastScrollTop && scrollTop > navbarHeight){
      // Scroll Down
      document.querySelector('.page-head').classList.remove('shown');
      document.querySelector('.page-head').classList.add('not-shown');
    } else {
      // Scroll Up
      if(scrollTop + window.outerHeight < document.documentElement.scrollHeight) {
          document.querySelector('.page-head').classList.remove('not-shown');
          document.querySelector('.page-head').classList.add('shown');
      }
    }

    lastScrollTop = scrollTop;
}
window.addEventListener('scroll', function(e) {
    didScroll = true;
});

window.setInterval(function() {
    if(didScroll) {
        hasScrolled();
        didScroll = false;
    }
});
