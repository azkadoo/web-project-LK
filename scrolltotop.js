let mybutton = document.getElementById("buttonToTop");

// When the user scrolls down 80px from the top of the document, show the button
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function scrollToTop() {
  document.documentElement.scrollTop = 0;
}
