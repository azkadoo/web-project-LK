
    function updateCharacterCounter($inputElement, $counterElement, maxLength) {
        $inputElement.on('input', function () {
            const currentLength = $inputElement.val().length;
            $counterElement.text(`${currentLength}/${maxLength}`);
        });
    }

    function validatePassword(selector, minLength, errorMessage) {
        const password = $(selector).val();
        if (password.length < minLength) {
            alert(errorMessage);
            return false;
        }
        return true;
    }

    // Setup Login Counters
    updateCharacterCounter($('#login-username'), $('#login-username-counter'), 20);
    updateCharacterCounter($('#login-email'), $('#login-email-counter'), 30);
    updateCharacterCounter($('#login-password'), $('#login-password-counter'), 10);

    // Setup Sign-up Counters
    updateCharacterCounter($('#username'), $('#username-counter'), 20);
    updateCharacterCounter($('#email-signup'), $('#email-signup-counter'), 30);
    updateCharacterCounter($('#password-signup'), $('#password-signup-counter'), 10);

    // Form Submission Handling
    $('#form-login').on('submit', function () {
        return validatePassword('#login-password', 8, 'Password login harus minimal 8 karakter!');
    });

    $('#form-signup').on('submit', function () {
        return validatePassword('#password-signup', 8, 'Password harus minimal 8 karakter!');
    });
    
    // Toggle between Login and Sign-Up
    $('#sign-up-btn').on('click', function () {
        $('.container').addClass('sign-up-mode');
    });

    $('#sign-in-btn').on('click', function () {
        $('.container').removeClass('sign-up-mode');
    });
;
