const topNav = document.getElementById('top-nav');
const toggleButton = document.getElementById('toggle-btn');
const bottomNav = document.getElementById('bottom-nav');

toggleButton.addEventListener('click', function () {
    topNav.classList.toggle('open'); // Toggle the "open" class on first navbar
});



function incrementStats() {
    const counters = document.querySelectorAll('.counter');

    counters.forEach((counter) => {
        counter.innerText = 0;

        const updateCounter = () => {
            const target = +counter.getAttribute('data-target');
            const c = +counter.innerText;

            const increment = target / 200;

            if (c < target) {
                counter.innerText = Math.ceil(c + increment);
                setTimeout(updateCounter, 1);
            } else {
                counter.innerText = target;
            }
        };
        updateCounter();
    });
}



document.addEventListener('DOMContentLoaded', incrementStats);


document.getElementById('increment-btn').addEventListener('click', function () {
    var quantityInput = document.getElementById('quantity');
    var currentValue = parseInt(quantityInput.value);

    if (currentValue < 10) { // Max value is 10
        quantityInput.value = currentValue + 1;
    }
});

document.getElementById('decrement-btn').addEventListener('click', function () {
    var quantityInput = document.getElementById('quantity');
    var currentValue = parseInt(quantityInput.value);

    if (currentValue > 1) { // Min value is 1
        quantityInput.value = currentValue - 1;
    }
});


$(document).ready(function () {
    $('.product-sync-init').slick({
        // ... other options
        zoom: true
    });
});


