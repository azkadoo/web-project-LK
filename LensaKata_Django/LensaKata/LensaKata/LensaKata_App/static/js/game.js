$(document).ready(function() {
    // Membuat div untuk menampung tag yang dipilih
    if (!$('.answer-tags').length) {
        $('.answer-container').prepend('<div class="answer-tags"></div>');
    }

    // Event listener untuk tag yang bisa diklik
    $('.tags').on('click', '.tag', function() {
        let $this = $(this);
        let $answerTags = $('.answer-tags');
        
        // Pindahkan tag ke answer-tags
        $this.detach().appendTo($answerTags);
        updateInputValue();
    });

    // Event listener untuk mengembalikan tag ke tags container
    $('.answer-tags').on('click', '.tag', function() {
        let $this = $(this);
        let $tags = $('.tags');
        
        // Kembalikan tag ke tags container
        $this.detach().appendTo($tags);
        updateInputValue();
    });

    // Fungsi untuk memperbarui nilai input tersembunyi
    function updateInputValue() {
        let tagTexts = $('.answer-tags .tag').map(function() {
            return $(this).text().trim();
        }).get();
        
        // Update hidden input dan text input
        $('#tags-input').val(tagTexts.join(' '));
        $('input[name="user_answer"]').val(tagTexts.join(' '));
        
        console.log("Updated tags value:", tagTexts.join(' '));
    }

    // Event listener untuk form submission
    $('form').on('submit', function(e) {
        updateInputValue();
        console.log("Submitting form with tags:", $('#tags-input').val());
    });
});