document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.review-container');
    const parentContainer = document.querySelector('.container-small.bg-blue');
    
    function updateScrollbar() {
        const scrollWidth = container.scrollWidth;
        const clientWidth = container.clientWidth;
        const scrollLeft = container.scrollLeft;
        
        // Hitung total lebar konten yang dapat di-scroll
        const scrollableWidth = scrollWidth - clientWidth;
        
        const thumbWidth = 20;  // Sesuaikan dengan lebar thumb yang Anda inginkan
        const maxTranslate = 90 - thumbWidth;  // 90 karena kita memiliki 5% padding di kedua sisi
        
        let translateX;
        
        if (scrollableWidth <= 0) {
            // Jika tidak ada konten yang bisa di-scroll, tempatkan thumb di ujung kanan
            translateX = maxTranslate;
        } else {
            // Hitung persentase scroll
            const scrollPercentage = (scrollLeft / scrollableWidth);
            translateX = scrollPercentage * maxTranslate;
            
            // Jika scroll hampir di akhir (toleransi 1px), tempatkan thumb di ujung kanan
            if (scrollLeft >= scrollableWidth - 1) {
                translateX = maxTranslate;
            }
        }

        parentContainer.style.setProperty('--scroll-translate', `translateX(${translateX}%)`);
    }

    container.addEventListener('scroll', updateScrollbar);
    window.addEventListener('resize', updateScrollbar);
    
    // Panggil fungsi saat halaman dimuat untuk mengatur posisi awal
    updateScrollbar();
});


// Dark Mode -------------------------
let darkmode = localStorage.getItem("darkmode");
const themeSwitch = document.getElementById("theme-switch");

const enableDarkMode = () => {
    document.body.classList.add("darkmode");
    localStorage.setItem("darkmode", "active");
};

const disableDarkMode = () => {
    document.body.classList.remove("darkmode");
    localStorage.setItem("darkmode", "inactive");
};

if (darkmode === "active") enableDarkMode();

themeSwitch.addEventListener("click", () => {
    darkmode = localStorage.getItem("darkmode");
    darkmode !== "active" ? enableDarkMode() : disableDarkMode();
});

// Scroll to Top -------------------------

const scrollToTopBtn = document.getElementById("scrollToTopBtn");

// event listener untuk memantau scroll halaman
window.addEventListener("scroll", () => {
    // jika posisi scroll lebih dari 20px, tampilkan tombol
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        scrollToTopBtn.style.display = "block";
    } else {
        // jika posisi scroll kurang dari 20px, sembunyikan tombol
        scrollToTopBtn.style.display = "none";
    }
});

// fungsi untuk scroll kembali ke atas
scrollToTopBtn.addEventListener("click", () => {
    // smooth scroll ke bagian paling atas halaman
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});


// let mybutton = document.getElementById("buttonToTop");

// window.onscroll = function () {
//     scrollFunction();
// };

// function scrollFunction() {
//     if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
//         mybutton.style.display = "block";
//     } else {
//         mybutton.style.display = "none";
//     }
// }

// function scrollToTop() {
//     document.documentElement.scrollTop = 0;
// }

// Carousel -------------------------
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

    // Panggil nextSlide setiap 3 detik untuk transisi otomatis
    setInterval(nextSlide, 3000);

});


