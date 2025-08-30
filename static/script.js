// Small interactivity
// DOM manipulation (querySelector, querySelectorAll)
// Event listeners (mouseenter, mouseleave, click)
// Smooth scrolling for UX

document.addEventListener("DOMContentLoaded", function () {
  // Add subtle animate to the APOD image on hover
  // DOM – Document Object Model:
  //An event listener that waits until the HTML document is fully loaded before running JS.
  //Ensures elements exist in the DOM before trying to access them and prevents errors.
  const apodImg = document.querySelector(".apod-card img");
  if (apodImg) {
    apodImg.addEventListener("mouseenter", () => apodImg.style.transform = "scale(1.02)");
    apodImg.addEventListener("mouseleave", () => apodImg.style.transform = "scale(1)");
    apodImg.style.transition = "transform 300ms ease";
  } // Adds a small zoom animation on hover. Improves user experience by making the UI feel dynamic and responsive.

  // Smooth scroll for navigation links
  document.querySelectorAll('.nav a').forEach(a => {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      const href = this.getAttribute('href');
      document.querySelector(href).scrollIntoView({ behavior: 'smooth' });
    });
  });
});

