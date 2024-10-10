// Tambahkan tombol yang bisa menampilkan atau menyembunyikan elemen di halaman, seperti menyembunyikan deskripsi fitur atau gambar testimonial.

 <button id="toggleButton">Sembunyikan Review</button>

document.addEventListener("DOMContentLoaded", function() {
    const toggleButton = document.getElementById("toggleButton");
    const reviewSection = document.querySelector(".review-section");

    toggleButton.addEventListener("click", function() {
        // Memeriksa apakah section saat ini terlihat atau tidak
        if (reviewSection.classList.contains("hidden")) {
            reviewSection.classList.remove("hidden")
            toggleButton.textContent = "Sembunyikan Review"
        } else {
            reviewSection.classList.add("hidden")
            toggleButton.textContent = "Tampilkan Review"
        }
    });
});
