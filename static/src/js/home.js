import Flickity from 'flickity';

const homeCarousel = document.querySelector('.home-intro');
const homeSlideCount = homeCarousel.childElementCount

if (homeSlideCount > 1) {
    const flkty = new Flickity(homeCarousel, {
      cellAlign: 'left',
      pageDots: false,
      autoPlay: 6000,
      wrapAround: homeSlideCount > 2 ? true : false,
      contain: homeSlideCount < 3 ? true : false
    });
}
