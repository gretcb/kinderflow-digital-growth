"use strict";

const FALLBACK_SIGN_DATA = {
  sign: "More",
  routine: ["Snack time", "Playtime"],
  age_range: "0-3",
  format: ["video", "routine card", "family guidance"],
  school_assignment: {
    classroom_group: "Group 1–2",
    tutors_included: 2,
    delivery: "existing school-family channel"
  },
  family_access: {
    included: "2 main tutors included",
    extra_caregiver: "Optional paid add-on",
    examples: ["Grandparent", "Nanny", "Second home"]
  },
  add_ons: ["printed flashcards", "original mini stories", "original short songs"],
  boundaries: [
    "No child video required",
    "Family guidance, not clinical advice",
    "Internal content production is managed by KinderFlow"
  ]
};

const setText = (selector, value) => {
  document.querySelectorAll(selector).forEach((element) => {
    element.textContent = value;
  });
};

const renderSignData = (data) => {
  setText("[data-sign-name]", data.sign);
  setText("[data-routine]", data.routine.join(" / "));
  setText("[data-age-range]", data.age_range);
  setText("[data-format]", data.format.map((item) => item.charAt(0).toUpperCase() + item.slice(1)).join(" + "));
};

const loadSignData = async () => {
  let data = FALLBACK_SIGN_DATA;
  try {
    const response = await fetch("data/approved_sign_more.json");
    if (response.ok) data = await response.json();
  } catch (_error) {
    // file:// blocks local fetch in many browsers; the equivalent embedded data keeps that mode usable.
  }
  renderSignData(data);
};

const routineButton = document.querySelector("#open-routine");
const routineDetail = document.querySelector("#routine-detail");

if (routineButton && routineDetail) {
  routineButton.addEventListener("click", () => {
    const isOpen = routineButton.getAttribute("aria-expanded") === "true";
    routineButton.setAttribute("aria-expanded", String(!isOpen));
    routineButton.textContent = isOpen ? "Open routine card" : "Close routine card";
    routineDetail.hidden = isOpen;
  });
}

document.querySelector("#print-family-card")?.addEventListener("click", () => window.print());

loadSignData();
