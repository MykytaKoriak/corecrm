document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("select").forEach((select) => {
    if (!select.classList.contains("form-control")) select.classList.add("form-select");
  });
});
