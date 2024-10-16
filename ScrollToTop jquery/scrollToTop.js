$(document).ready(function() {
    // Tampilkan tombol saat pengguna menggulir ke bawah
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#scrollToTop').fadeIn();
        } else {
            $('#scrollToTop').fadeOut();
        }
    });

    // Fungsi untuk menggulir ke atas halaman
    $('#scrollToTop').click(function() {
        $('html, body').animate({scrollTop : 0},10);
        return false;
    });
});