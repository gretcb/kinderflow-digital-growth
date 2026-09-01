"use strict";

const createMenu = document.querySelector("[data-create-menu]");

if (createMenu) {
  const trigger = createMenu.querySelector(".create-menu-trigger");
  const options = createMenu.querySelector(".create-menu-options");
  const links = Array.from(options.querySelectorAll("a"));

  const closeMenu = ({ returnFocus = false } = {}) => {
    trigger.setAttribute("aria-expanded", "false");
    options.hidden = true;
    if (returnFocus) trigger.focus();
  };

  const openMenu = () => {
    trigger.setAttribute("aria-expanded", "true");
    options.hidden = false;
    links[0]?.focus();
  };

  trigger.addEventListener("click", () => {
    if (trigger.getAttribute("aria-expanded") === "true") closeMenu();
    else openMenu();
  });

  createMenu.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      event.preventDefault();
      closeMenu({ returnFocus: true });
    }
  });

  document.addEventListener("click", (event) => {
    if (!createMenu.contains(event.target)) closeMenu();
  });
}
