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
    included: "2 main caregivers included",
    extra_caregiver: "Optional extra caregiver access",
    examples: ["Grandparent", "Nanny", "Second home"]
  },
  add_ons: ["printed flashcards", "original mini stories", "original short songs"],
  boundaries: [
    "Reviewed reference source",
    "Family guidance for familiar routines",
    "Content is prepared and reviewed by KinderFlow"
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

const applyReviewedFamilyPreview = () => {
  if (new URLSearchParams(window.location.search).get("reviewed") !== "1") return;
  try {
    const content = JSON.parse(sessionStorage.getItem("kinderflowReviewedContentPack") || "null");
    if (content?.review_status !== "APPROVED" || content?.human_review?.approved !== true) return;
    const label = content.flashcard_copy?.primary_label || content.sign_id?.toUpperCase();
    if (label) setText("[data-sign-name]", label);
    if (content.routine_context?.en) setText("[data-family-routine]", `${content.routine_context.en}. Continue the same reviewed cue at home.`);
    if (content.family_guidance?.en) setText("[data-family-guidance]", content.family_guidance.en);
    if (content.try_it_during?.en) setText("[data-family-try]", content.try_it_during.en);
    if (content.family_message?.en) setText("[data-school-home-copy]", content.family_message.en);
  } catch (_error) {
    // Invalid or absent session content leaves the reviewed human-authored preview unchanged.
  }
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
    routineButton.textContent = isOpen ? "Show routine card" : "Hide routine card";
    routineDetail.hidden = isOpen;
  });
}

document.querySelector("#print-family-card")?.addEventListener("click", () => window.print());

loadSignData().finally(applyReviewedFamilyPreview);
