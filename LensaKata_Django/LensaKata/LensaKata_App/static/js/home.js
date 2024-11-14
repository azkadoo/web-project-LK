
// Index Page
$(document).ready(function() {
    // Scroll to Top Button
    const $scrollToTopBtn = $('#scrollToTopBtn');

    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $scrollToTopBtn.fadeIn(); // Show button
        } else {
            $scrollToTopBtn.fadeOut(); // Hide button
        }
    });

    $scrollToTopBtn.click(function() {
        $('html, body').animate({ scrollTop: 0 }, 300); // Smooth scroll to top
    });

    // Carousel Auto Slide
    let autoSlide = setInterval(() => {
        $('#carouselExampleIndicators .carousel-control-next').click(); // Move to the next item in the carousel
    }, 3000);

    // Carousel Control Buttons
    $('.carousel-control-next, .carousel-control-prev').click(function() {
        clearInterval(autoSlide);
        autoSlide = setInterval(() => {
            $('#carouselExampleIndicators .carousel-control-next').click(); // Move to the next item in the carousel
        }, 3000);
    });

    // Dark Mode
    const $themeSwitch = $('#theme-switch');
    const darkmode = localStorage.getItem("darkmode");

    if (darkmode === "active") {
        $('body').addClass("darkmode"); // Add dark mode class
    }

    $themeSwitch.click(function() {
        $('body').toggleClass("darkmode"); // Toggle dark mode class
        localStorage.setItem("darkmode", $('body').hasClass("darkmode") ? "active" : "inactive");
    });
});
