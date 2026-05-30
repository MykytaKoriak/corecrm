document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("select").forEach((select) => {
    if (!select.classList.contains("form-control")) select.classList.add("form-select");
  });
  document.querySelectorAll(".filter-bar select").forEach((select) => {
    select.addEventListener("change", () => select.form?.requestSubmit());
  });
});
