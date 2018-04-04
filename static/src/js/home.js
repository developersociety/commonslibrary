import Flickity from 'flickity';

const homeCarousel = document.querySelector('.home-intro');
const homeSlideCount = homeCarousel.childElementCount

const flkty = new Flickity(homeCarousel, {
  cellAlign: 'left',
  prevNextButtons: false,
  pageDots: false,
  autoPlay: 6000,
  wrapAround: homeSlideCount > 2 ? true : false,
  contain: homeSlideCount < 3 ? true : false
});
