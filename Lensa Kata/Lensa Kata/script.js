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