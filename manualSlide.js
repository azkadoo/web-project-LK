// carousel manual
// Menangani interaksi pengguna dengan addEventListener untuk tombol navigasi.

document.addEventListener('DOMContentLoaded', function () {
    const carouselItems = document.querySelectorAll('.carousel-item');
    const indicators = document.querySelectorAll('.carousel-indicators button');
    let currentIndex = 0;

    function updateCarousel(index) {
        carouselItems.forEach((item, i) => {
            item.classList.toggle('active', i === index);
        });
        indicators.forEach((indicator, i) => {
            indicator.classList.toggle('active', i === index);
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % carouselItems.length;
        updateCarousel(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + carouselItems.length) % carouselItems.length;
        updateCarousel(currentIndex);
    }

    document.querySelector('.carousel-control-next').addEventListener('click', nextSlide);
    document.querySelector('.carousel-control-prev').addEventListener('click', prevSlide);
});
