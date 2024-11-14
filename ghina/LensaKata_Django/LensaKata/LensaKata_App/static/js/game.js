    // Timer 
    let remainingTime = 60;
    const levelText = $(".level").text();

    const updateLevelText = () => {
        $(".level").text(`${levelText} - Waktu Tersisa: ${remainingTime}s`);
    };

    updateLevelText();
    
    const intervalTimer = setInterval(() => {
        if (remainingTime > 0) {
            remainingTime--;
            updateLevelText();
        } else {
            clearInterval(intervalTimer);
            showTimeUpOverlay();
        }
    }, 1000);

// Function to show the overlay when time is up
function showTimeUpOverlay() {
    // Create overlay div
    const $overlay = $('<div></div>').css({
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        zIndex: 1000
    });

    // Create message and button inside overlay
    const $message = $('<h2>Waktu habis! Anda akan diarahkan ke beranda</h2>');
    const $button = $('<button>OK</button>').css({
        padding: '10px 20px',
        fontSize: '16px',
        marginTop: '20px'
    }).on('click', function() {
        window.location.href = "index.html"; // Redirect on button click
    });

    // Append message and button to overlay, and overlay to body
    $overlay.append($message, $button);
    $('body').append($overlay);
}

    // Definisikan jawaban yang benar
    const correctAnswer = ['Jaka Tarub', 'mengambil', 'selendang'];

    // Event listener untuk tombol submit
    $('#submit-answer').on('click', function() {
        validateAnswer();
    });

    // Fungsi untuk memvalidasi jawaban
    function validateAnswer() {
        let userAnswer = $('.answer-tags .tag').map(function() {
            return $(this).text().trim();
        }).get();

        // Periksa apakah semua kata dalam jawaban yang benar ada dalam jawaban pengguna
        let isCorrect = correctAnswer.every(word => userAnswer.includes(word));

        if (isCorrect) {
            alert('Selamat! Jawaban Anda benar.');
            // Di sini Anda bisa menambahkan logika untuk pindah ke level selanjutnya atau menampilkan skor
        } else {
            alert('Maaf, jawaban Anda belum tepat. Silakan coba lagi.');
        }
    }

    // Fungsi untuk memperbarui nilai input
    function updateInputValue() {
        let $input = $('.answer-container input');
        let tagTexts = $('.answer-tags .tag').map(function () {
            return $(this).text().trim();
        }).get();
        $input.val(tagTexts.join(' '));
    }

    // Event listener untuk tag yang bisa diklik
    $('.tags').on('click', '.tag', function () {
        let $this = $(this);
        let $answerTags = $('.answer-tags');

        $this.detach().appendTo($answerTags);
        updateInputValue();
    });

    $('.answer-tags').on('click', '.tag', function () {
        let $this = $(this);
        let $tags = $('.tags');

        $this.detach().appendTo($tags);
        updateInputValue();
    });
