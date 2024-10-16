// carousel yang secara otomatis menampilkan berbagai poster atau gambar, dengan transisi antar gambar yang halus
//jQuery

$(document).ready(function() {
// Mulai carousel
let carousel = $('#carouselExampleIndicators');

    // Interval 3 detik
    let autoSlide = setInterval(function() {
        carousel.carousel('next');
    }, 3000);

    // Stop auto-sliding ketika user  mengklik tombol prev/next
    $('.carousel-control-next, .carousel-control-prev').click(function() {
        clearInterval(autoSlide);  // Stop auto-sliding saat diklik secara manual
        autoSlide = setInterval(function() {  // Restarts auto-sliding
        carousel.carousel('next');
        }, 3000);
    });
});