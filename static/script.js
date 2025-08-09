// Small interactivity + subtle star twinkle background generation (pure CSS fallback used here)
document.addEventListener("DOMContentLoaded", function () {
  // Add subtle animate to the APOD image on hover
  const apodImg = document.querySelector(".apod-card img");
  if (apodImg) {
    apodImg.addEventListener("mouseenter", () => apodImg.style.transform = "scale(1.02)");
    apodImg.addEventListener("mouseleave", () => apodImg.style.transform = "scale(1)");
    apodImg.style.transition = "transform 300ms ease";
  }

  // Smooth scroll for nav links
  document.querySelectorAll('.nav a').forEach(a => {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      const href = this.getAttribute('href');
      document.querySelector(href).scrollIntoView({ behavior: 'smooth' });
    });
  });
});

