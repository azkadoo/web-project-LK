
    /*
    // // Definisikan jawaban yang benar
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
    });*/