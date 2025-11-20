document.addEventListener("DOMContentLoaded", () => {
  function toggleAccordion(num) {
    const items = document.querySelectorAll(".accordion-item");
    items.forEach((item, index) => {
      const c = document.getElementById("acc" + (index + 1));
      if (index + 1 === Number(num)) {
        c.classList.toggle("open");
        item.classList.toggle("active");
      } else {
        c.classList.remove("open");
        item.classList.remove("active");
      }
    });
  }

  document.querySelectorAll(".accordion-header").forEach(header => {
    header.addEventListener("click", () => {
      toggleAccordion(header.dataset.num);
    });
  });
});
