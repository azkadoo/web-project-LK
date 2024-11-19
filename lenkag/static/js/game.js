$(document).ready(function () {
    $('#gameForm').on('submit', function (e) {
        e.preventDefault();

        const userInput = $('input[name="user_input"]').val();

        // Kirim data menggunakan AJAX
        $.ajax({
            url: '',
            method: 'POST',
            data: {
                user_input: userInput,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                $('#feedback').text(response.message);
                $('input[name="user_input"]').val('');
            },
            error: function (xhr) {
                const errorMessage = xhr.responseJSON?.error || 'An error occurred.';
                $('#feedback').text(errorMessage);
            }
        });
    });
});
