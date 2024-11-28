$(document).ready(function () {
    const currentPage = window.location.pathname.split('/').pop();

    if (currentPage === 'index.html') {
        // Scroll to Top Button
        $(window).scroll(function() {
            if ($(this).scrollTop() > 100) {
                $('#scrollToTopBtn').fadeIn(); 
            } else {
                $('#scrollToTopBtn').fadeOut();
            }
        });

        $('#scrollToTopBtn').click(function() {
            $('html, body').animate({scrollTop: 0}, 10);
        });

        // Carousel Auto Slide
        let autoSlide = setInterval(() => {
            $('#carouselExampleIndicators').carousel('next');
        }, 3000);

        $('.carousel-control-next, .carousel-control-prev').click(function() {
            clearInterval(autoSlide);
            autoSlide = setInterval(() => $('#carouselExampleIndicators').carousel('next'), 3000);
        });

        // Dark Mode
        const themeSwitch = $("#theme-switch");
        const darkmode = localStorage.getItem("darkmode");

        if (darkmode === "active") {
            $("body").addClass("darkmode");
        }

        themeSwitch.on("click", function() {
            $("body").toggleClass("darkmode");
            localStorage.setItem("darkmode", $("body").hasClass("darkmode") ? "active" : "inactive");
        });
    }
});