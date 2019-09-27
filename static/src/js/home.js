import Flickity from 'flickity';

const homeCarousel = document.querySelector('.home-intro');
const homeSlideCount = homeCarousel.childElementCount;
const prevButton = document.querySelector('.flickity-button.previous');
const nextButton = document.querySelector('.flickity-button.next');

const flkty = new Flickity(homeCarousel, {
    cellAlign: 'left',
    pageDots: false,
    autoPlay: 6000,
    wrapAround: homeSlideCount > 2,
    contain: homeSlideCount < 3,
    prevNextButtons: false
});

prevButton.onclick = (e) => {
    flkty.previous();
};

nextButton.onclick = (e) => {
    flkty.next();
};

// if wrap isn't enabled and at end, add class to button
if (homeSlideCount == 2) {
    flkty.on('select', (index) => {
        if (index == homeSlideCount - 1) {
            nextButton.disabled = true;
            prevButton.disabled = false;
        } else {
            prevButton.disabled = true;
            nextButton.disabled = false;
        }
    });
}
