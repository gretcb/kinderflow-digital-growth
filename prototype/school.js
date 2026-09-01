"use strict";

const GROUP_CHILDREN = {
  "Group 0–1": ["Child A", "Child B"],
  "Group 1–2": ["Child C", "Child D"],
  "Group 2–3": ["Child E", "Child F"]
};

const assignmentForm = document.querySelector("#school-assignment-form");
const signSelect = document.querySelector("#assignment-sign");
const groupSelect = document.querySelector("#assignment-group");
const childSelect = document.querySelector("#assignment-child");
const assignmentStatus = document.querySelector("#school-assignment-status");
const assignAnother = document.querySelector("#assign-another");
const activeList = document.querySelector("#active-sign-list");

const populateChildren = () => {
  const options = [new Option("All children in group", ""), ...GROUP_CHILDREN[groupSelect.value].map((child) => new Option(child, child))];
  childSelect.replaceChildren(...options);
};

const addActiveAssignment = (sign, target) => {
  const article = document.createElement("article");
  article.dataset.activeAssignment = "";
  article.innerHTML = `<div><span class="content-type-tag">Sign</span><h3>${sign}</h3><p>${target}</p></div><div><span class="status-pill status-ready">Active</span><button class="text-link-button" type="button" data-remove-assignment>Remove</button></div>`;
  activeList.appendChild(article);
};

if (assignmentForm) {
  groupSelect.addEventListener("change", populateChildren);
  document.querySelectorAll("[data-select-library-sign]").forEach((button) => {
    button.addEventListener("click", () => {
      signSelect.value = button.dataset.selectLibrarySign;
      assignmentStatus.textContent = `${signSelect.value} selected. Choose a group and confirm.`;
      assignAnother.hidden = true;
      assignmentForm.scrollIntoView({ behavior: "smooth", block: "start" });
      groupSelect.focus({ preventScroll: true });
    });
  });
  assignmentForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const child = childSelect.value;
    const target = child ? `${child} in ${groupSelect.value}` : `${groupSelect.value} · All children`;
    assignmentStatus.textContent = `${signSelect.value} assigned to ${target}. Family content is ready to share.`;
    addActiveAssignment(signSelect.value, target);
    assignAnother.hidden = false;
  });
  assignAnother.addEventListener("click", () => {
    signSelect.selectedIndex = 0;
    childSelect.value = "";
    assignmentStatus.textContent = `Group preserved: ${groupSelect.value}. Select another sign or content item.`;
    assignAnother.hidden = true;
    signSelect.focus();
  });
  populateChildren();
}

activeList?.addEventListener("click", (event) => {
  const removeButton = event.target.closest("[data-remove-assignment]");
  if (removeButton) removeButton.closest("[data-active-assignment]").remove();
});

const addonForm = document.querySelector("#school-addon-form");
const addonSelect = document.querySelector("#school-addon");
const addonAction = document.querySelector("#school-addon-action");
const addonScope = document.querySelector("#school-addon-scope");
const addonTarget = document.querySelector("#school-addon-target");
const addonSubmit = document.querySelector("#school-addon-submit");
const addonStatus = document.querySelector("#school-addon-status");

if (addonForm) {
  const groups = Object.keys(GROUP_CHILDREN);
  const children = Object.values(GROUP_CHILDREN).flat();
  const updateAddon = () => {
    const targets = addonScope.value === "child" ? children : groups;
    addonTarget.replaceChildren(...targets.map((target) => new Option(target, target)));
    addonSubmit.textContent = addonAction.value === "enabled" ? "Enable add-on" : "Disable add-on";
    addonStatus.textContent = "";
  };
  addonAction.addEventListener("change", updateAddon);
  addonScope.addEventListener("change", updateAddon);
  addonForm.addEventListener("submit", (event) => {
    event.preventDefault();
    addonStatus.textContent = `${addonSelect.value} ${addonAction.value} for ${addonTarget.value} in this static prototype.`;
  });
  updateAddon();
}
