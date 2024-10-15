// membuat event handler yang menangani perubahan warna background saat tombol diklik.
      <!-- jQuery CDN -->
      <script
        src="https://code.jquery.com/jquery-3.7.1.js"
        integrity="sha256-eKhayi8LEQwp4NKxN+CfCh+3qOVUtJn3QNZ0TciWLP4="
        crossorigin="anonymous"
      ></script>

      <!-- Dark Mode -->
      <script>
        let darkmode = localStorage.getItem("darkmode"); //Untuk localStorage tidak ada metode khusus di jQuery untuk mengelolanya.
        const themeSwitch = $("#theme-switch"); // Menggunakan jQuery untuk memilih elemen

        const enableDarkMode = () => {
          $("body").addClass("darkmode"); // Menambahkan class "darkmode" ke body dengan jQuery
          localStorage.setItem("darkmode", "active");
        };
        const disableDarkMode = () => {
          $("body").removeClass("darkmode"); // Menghapus class "darkmode" dari body dengan jQuery
          localStorage.setItem("darkmode", "inactive");
        };

        if (darkmode === "active") {
          enableDarkMode();
        }

        themeSwitch.on("click", function () {
          darkmode = localStorage.getItem("darkmode");
          if (darkmode !== "active") {
            enableDarkMode();
          } else {
            disableDarkMode();
          }
        });
      </script>
