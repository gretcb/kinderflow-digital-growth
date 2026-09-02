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
const assignmentSummary = document.querySelector("#assignment-summary");
const assignmentSubmit = document.querySelector("#assignment-submit");
const assignmentResult = document.querySelector(".assignment-result");
const assignAnother = document.querySelector("#assign-another");
const activeList = document.querySelector("#active-sign-list");

const reviewedDelivery = (() => {
  if (new URLSearchParams(window.location.search).get("reviewed") !== "1") return null;
  try {
    const value = JSON.parse(sessionStorage.getItem("kinderflowReviewedContentPack") || "null");
    return value?.review_status === "APPROVED" && value?.human_review?.approved === true ? value : null;
  } catch (_error) {
    return null;
  }
})();

const populateChildren = () => {
  const options = [new Option("All children in group", ""), ...GROUP_CHILDREN[groupSelect.value].map((child) => new Option(child, child))];
  childSelect.replaceChildren(...options);
  updateAssignmentSummary();
};

const updateAssignmentSummary = () => {
  const sign = signSelect.value;
  const group = groupSelect.value;
  const child = childSelect.value;
  assignmentSummary.textContent = child
    ? `${sign} will be assigned to ${child} in ${group}.`
    : `${sign} will be assigned to all children in ${group}.`;
  assignmentSubmit.textContent = child ? `Assign ${sign} to ${child}` : `Assign ${sign} to ${group}`;
};

const addActiveAssignment = (sign, target) => {
  const article = document.createElement("article");
  article.dataset.activeAssignment = "";
  article.innerHTML = `<div><span class="content-type-tag">Sign</span><h3>${sign}</h3><p>${target}</p></div><div><span class="status-pill status-ready">Active</span><button class="text-link-button" type="button" data-remove-assignment>Remove</button></div>`;
  activeList.appendChild(article);
};

if (assignmentForm) {
  groupSelect.addEventListener("change", populateChildren);
  signSelect.addEventListener("change", updateAssignmentSummary);
  childSelect.addEventListener("change", updateAssignmentSummary);
  document.querySelectorAll("[data-select-library-sign]").forEach((button) => {
    button.addEventListener("click", () => {
      signSelect.value = button.dataset.selectLibrarySign;
      assignmentResult.hidden = true;
      updateAssignmentSummary();
      assignmentForm.scrollIntoView({ behavior: "smooth", block: "start" });
      groupSelect.focus({ preventScroll: true });
    });
  });
  assignmentForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const child = childSelect.value;
    const target = child ? `${child} in ${groupSelect.value}` : `${groupSelect.value} · All children`;
    assignmentStatus.textContent = child
      ? `${signSelect.value} was assigned to ${child} in ${groupSelect.value}.`
      : `${signSelect.value} was assigned to ${groupSelect.value}.`;
    addActiveAssignment(signSelect.value, target);
    assignmentResult.hidden = false;
    assignmentResult.focus?.();
  });
  assignAnother.addEventListener("click", () => {
    signSelect.selectedIndex = 0;
    childSelect.value = "";
    assignmentStatus.textContent = "";
    assignmentResult.hidden = true;
    updateAssignmentSummary();
    signSelect.focus();
  });
  populateChildren();
  if (reviewedDelivery) {
    const label = reviewedDelivery.flashcard_copy?.primary_label || reviewedDelivery.sign_id.toUpperCase();
    signSelect.value = label;
    assignmentStatus.textContent = `${label} reviewed wording received from KinderFlow Content Studio. Choose a fictional group or child.`;
    updateAssignmentSummary();
  }
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
  const updateAddonLabel = () => {
    const verb = addonAction.value === "enabled" ? "Enable" : "Disable";
    addonSubmit.textContent = `${verb} ${addonSelect.value} for ${addonTarget.value}`;
    addonStatus.textContent = "";
  };
  const populateAddonTargets = () => {
    const targets = addonScope.value === "child" ? children : groups;
    addonTarget.replaceChildren(...targets.map((target) => new Option(target, target)));
    updateAddonLabel();
  };
  addonAction.addEventListener("change", updateAddonLabel);
  addonSelect.addEventListener("change", updateAddonLabel);
  addonScope.addEventListener("change", populateAddonTargets);
  addonTarget.addEventListener("change", updateAddonLabel);
  addonForm.addEventListener("submit", (event) => {
    event.preventDefault();
    addonStatus.textContent = `${addonSelect.value} ${addonAction.value} for ${addonTarget.value} in this static prototype.`;
  });
  populateAddonTargets();
}
