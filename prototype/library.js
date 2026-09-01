"use strict";

const filterButtons = Array.from(document.querySelectorAll("[data-library-filter]"));
const libraryRows = Array.from(document.querySelectorAll("[data-content-type]"));
const resultCount = document.querySelector("#library-result-count");

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.libraryFilter;
    let visible = 0;
    filterButtons.forEach((candidate) => candidate.setAttribute("aria-pressed", String(candidate === button)));
    libraryRows.forEach((row) => {
      const show = filter === "all" || row.dataset.contentType === filter;
      row.hidden = !show;
      if (show) visible += 1;
    });
    resultCount.textContent = `${visible} ${visible === 1 ? "item" : "items"} shown`;
  });
});
