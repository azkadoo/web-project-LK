const storyText = $('#story-text');
const approveBtn = $('#approve-btn');
const changeBtn = $('<button class="btn btn-outline-secondary ms-2" id="edit-btn">Ubah</button>');
const saveBtn = $('<button class="btn btn-outline-secondary ms-2" id="save-btn">Simpan</button>');
const approvalStatus = $('<p class="me-3">3 orang udah setuju!</p>');

// Tambahkan tombol ubah di sebelah kanan tombol setuju
approveBtn.after(changeBtn);

// Tambahkan keterangan setuju di sebelah kiri tombol setuju
approveBtn.before(approvalStatus);

// Event untuk tombol ubah (mengubah <p> menjadi <input>)
changeBtn.on('click', function () {
    const currentText = storyText.text();
    const inputField = $('<input type="text" class="form-control mt-2" id="story-input">').val(currentText);
    storyText.replaceWith(inputField);
    changeBtn.hide();
    approveBtn.after(saveBtn);
});

// Event untuk tombol simpan (mengubah kembali <input> menjadi <p>)
saveBtn.on('click', function () {
    const newText = $('#story-input').val();
    const newStoryText = $('<p id="story-text" class="mt-2"></p>').text(newText);
    $('#story-input').replaceWith(newStoryText);
    saveBtn.remove();
    changeBtn.show();
});

// Event untuk tombol setuju (mengubah "Setuju" menjadi "Selesaikan")
approveBtn.on('click', function () {
    approveBtn.text('Selesaikan');
    // Tambahkan logika untuk menyelesaikan cerita
    alert('Cerita sudah selesai. Terima kasih!');
});
