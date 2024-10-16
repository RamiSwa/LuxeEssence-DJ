$(document).ready(function () {
    // Initialize Slick Slider
    $('.product-slider-init').slick({
        slidesToShow: 3, // Show 4 products at a time
        slidesToScroll: 1, // Scroll 1 product at a time
        infinite: true, // Infinite scrolling
        arrows: true, // Show navigation arrows
        prevArrow: '<button class="slick-prev"><i class="fas fa-chevron-left"></i></button>',
        nextArrow: '<button class="slick-next"><i class="fas fa-chevron-right"></i></button>',
        responsive: [{
                breakpoint: 1024, // For smaller devices
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 768, // For tablet devices
                settings: {
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 576, // For mobile devices
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });
});
