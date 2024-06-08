"use strict"

window.addEventListener('load', () => {

  // document.querySelectorAll('.header__sub-menu-left-link').forEach(item => {
  //   item.addEventListener('mouseover', (e) => {
  //     const dataMenu = item.dataset.menu;
  //     document.querySelectorAll('.header__sub-menu-left-link').forEach(item1 => {
  //       item1.classList.remove('active');
  //     });
  //     item.classList.add('active');
  //     document.querySelectorAll('.header__sub-menu-right-content').forEach(subitem => {
  //       subitem.classList.remove('active');
  //     });
  //     try {
  //       document.querySelector('#'+dataMenu).classList.add('active')
  //     } catch (error) {
  //       console.log(error);
  //     }
  //   });
  // });

  // document.querySelectorAll('.header__sub-menu-by-games-link').forEach(item => {
  //   item.addEventListener('mouseover', (e) => {
  //     const dataMenu = item.dataset.menu;
  //     document.querySelectorAll('.header__sub-menu-by-games-link').forEach(item1 => {
  //       item1.classList.remove('active');
  //     });
  //     item.classList.add('active');
  //     document.querySelectorAll('.header__sub-menu-by-games-right').forEach(subitem => {
  //       subitem.classList.remove('active');
  //     });
  //     try {
  //       document.querySelector('#'+dataMenu).classList.add('active')
  //     } catch (error) {
  //       console.log(error);
  //     }
  //   });
  // });


  const recSlider = new Swiper('.reclams-banner__slider', {
    slidesPerView: 3,
    spaceBetween: 14,
    speed: 1000,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },

    breakpoints: {
      100: {
        slidesPerView: 1.5,
        spaceBetween: 8,
        centeredSlides: true,
        loop: true,
        currentSlide: 1,
      },
      680: {
        slidesPerView: 1.8,
        spaceBetween: 12,
        centeredSlides: true,
        loop: true,
        currentSlide: 1,
      },
      900: {
        slidesPerView: 3,
        spaceBetween: 12,
        loop: true,
      },
      1441: {
        loop: true,
        slidesPerView: 3,
        spaceBetween: 14,
      },
    }
  });

  const topsSlider = new Swiper('.tops-section__slider', {
    slidesPerView: 3,
    spaceBetween: 12,
    enabled: false,
    // centeredSlides: true,
    // loop: true,
    // speed: 500,

    pagination: {
      el: '.tops-section__pagination',
      type: 'bullets',
      clickable: true,
    },

    breakpoints: {
      100: {
        slidesPerView: 'auto',
        spaceBetween: 10,
        enabled: true,
      },
      761: {
        spaceBetween: 10,
        // slidesPerView: 'auto',
        slidesPerView: 3,
        enabled: false,
      },
      900: {
        slidesPerView: 3,
        spaceBetween: 12,
        enabled: false,
      },
      1441: {
        slidesPerView: 3,
        spaceBetween: 20,
        enabled: false,
      },
    }
  });

  const blogSlider = new Swiper('.blog-slider__swiper', {
    slidesPerView: 'auto',
    spaceBetween: 20,
    centeredSlides: true,
    loop: true,
    loopedSlides: 10,
    speed: 500,

    navigation: {
      nextEl: '.blog-slider__button_next',
      prevEl: '.blog-slider__button_prev',
    },

    pagination: {
      el: '.blog-slider__pagination',
      type: 'bullets',
      clickable: true,
    },

    breakpoints: {
      100: {
        spaceBetween: 12,
      },
      1000: {
        spaceBetween: 20,
      },
    }
  });

  const mediaSlider = new Swiper('.media-slider__swiper', {
    slidesPerView: 'auto',
    spaceBetween: 20,
    loop: true,
    loopedSlides: 10,
    speed: 500,
    centeredSlides: true,

    navigation: {
      nextEl: '.media-slider__button_next',
      prevEl: '.media-slider__button_prev',
    },

    pagination: {
      el: '.media-slider__pagination',
      type: 'bullets',
      clickable: true,
    },

    breakpoints: {
      100: {
        spaceBetween: 10,
      },
      1000: {
        spaceBetween: 20,
      },
    }
  });

  const partnersSlider = new Swiper('.partners-slider__swiper', {
    slidesPerView: 'auto',
    speed: 8000,
    a11y: false,
    spaceBetween: 12,
    loop: true,
    centeredSlides: true,
    // allowTouchMove: false,
    autoplay: {
      delay: 0,
      disableOnInteraction: false,
      pauseOnMouseEnter: true,
    },

    breakpoints: {
      100: {
        spaceBetween: 5,
      },
      600: {
        spaceBetween: 10,
      },
      1000: {
        spaceBetween: 12,
      },
    }
  });


  const predictionSlider = new Swiper('.latest-prediction__grid', {
    slidesPerView: 'auto',
    spaceBetween: 0,
    enabled: false,
    centeredSlides: false,
    loop: false,

    breakpoints: {
      100: {
        slidesPerView: 'auto',
        spaceBetween: 10,
        enabled: true,
        centeredSlides: true,
        loop: true,
        pagination: {
          el: '.latest-prediction__pagination',
          type: 'bullets',
          clickable: true,
        },
      },

      761: {
        slidesPerView: 'auto',
        spaceBetween: 0,
        enabled: false,
        centeredSlides: false,
        loop: false,
      },
    }
  });

  const keepLearnSlider = new Swiper('.keep-learning__slider', {
    slidesPerView: 4,
    spaceBetween: 10,
    enabled: false,
    centeredSlides: false,
    loop: false,

    breakpoints: {
      100: {
        slidesPerView: 'auto',
        spaceBetween: 10,
        enabled: true,
        centeredSlides: false,
        loop: true,
        pagination: {
          el: '.latest-prediction__pagination',
          type: 'bullets',
          clickable: true,
        },
      },

      1021: {
        slidesPerView: 4,
        spaceBetween: 10,
        enabled: false,
        centeredSlides: false,
        loop: false,
      },
    }
  });


  const statisticSlider = new Swiper('.promote-stats__swiper', {
    slidesPerView: 'auto',
    spaceBetween: 24,
    loop: false,
    speed: 500,

    navigation: {
      nextEl: '.promote-stats__swiper-button_next',
      prevEl: '.promote-stats__swiper-button_prev',
    },

    pagination: {
      el: '.promote-stats__swiper-pagination',
      type: 'bullets',
      clickable: true,
    },

    breakpoints: {
      100: {
        spaceBetween: 10,
      },
      1000: {
        spaceBetween: 20,
      },
    }
  });
});
