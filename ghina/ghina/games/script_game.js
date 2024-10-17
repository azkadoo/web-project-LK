// logika untuk game: logika timer, validasi jawaban

$(document).ready(function() { 
    let remainingTime = 60;
    const levelText = $(".level").text();

    // Fungsi untuk memperbarui teks level dengan waktu tersisa
    const updateLevelText = () => {
        $(".level").text(`${levelText} - Waktu Tersisa: ${remainingTime}s`);
    };

    updateLevelText(); // Pembaruan awal

    // Logika Timer
    const intervalTimer = setInterval(() => {
        if (remainingTime > 0) {
            remainingTime--;
            updateLevelText(); // Perbarui setiap detik
        } else {
            clearInterval(intervalTimer);
            alert("Waktu habis! Anda akan diarahkan ke beranda");
        }
    }, 1000);

    // Validasi jawaban ketika tombol diklik
    $(".button-key").click(function() {
        const userAnswer = $(".answer input").val().trim().toLowerCase();
        const correctAnswer = "jaka tarub mengambil selendang bidadari";

        if (userAnswer === correctAnswer) {
            $(".answer input").css("outline", "2px solid #59e379");
            setTimeout(() => alert("Jawaban benar!"), 100); // Tampilkan alert setelah penundaan
        } else {
            shakeInput(); // Panggil animasi goyang untuk jawaban salah
        }
    });

    // Hapus warna outline saat ada perubahan di input
    $(".answer input").on("input", function() {
        $(this).css("outline", "none"); // Kembalikan outline ke default
    });

    // Animasi shake untuk jawaban salah
    function shakeInput() {
        $(".answer input").addClass("shake");
        setTimeout(() => {
            $(".answer input").removeClass("shake"); // Hapus animasi setelah 500ms
        }, 500);
    }
});