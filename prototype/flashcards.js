"use strict";

const REQUIRED_SIGN_FIELDS = [
  "id", "sign_id", "display_name", "spanish_label", "routine", "approved_source_context",
  "short_family_guidance", "try_it_during", "teacher_message", "family_message",
  "generation_method", "content_status", "publication_status", "school_visibility", "flashcard_status",
  "video_asset", "character_asset", "hand_pose_asset", "movement_reference",
  "school_pack_required", "printable", "image_export_available", "last_reviewed",
  "review_status"
];

const OUTPUT_COPY = {
  en: { language: "English", routine: "Routine", guidance: "How to use it" },
  es: { language: "Spanish", routine: "Rutina", guidance: "Cómo usarlo" }
};

const MORE_ROUTINE_COPY = {
  en: { routine: "Snack time", guidance: "Use the sign naturally just before offering more food." },
  es: { routine: "Hora de la merienda", guidance: "Haz el signo de forma natural justo antes de ofrecer más comida." }
};

const builder = {
  signs: [], selectedId: null, language: "en", cardType: "flashcard",
  layoutReviewed: false, reviewedHandoff: null
};

const card = document.querySelector(".flashcard-output");
const signSelect = document.querySelector("#published-sign");
const previewEmpty = document.querySelector("#preview-empty");
const previewTitle = document.querySelector("#preview-title");
const state = document.querySelector("#flashcard-state");
const status = document.querySelector("#builder-status");
const reviewStateText = document.querySelector("#review-state-text");
const reviewButton = document.querySelector("#review-flashcard");
const printButton = document.querySelector("#print-flashcard");
const preApprovalActions = document.querySelector("#pre-approval-actions");
const postApprovalActions = document.querySelector("#post-approval-actions");

const validateSignData = (payload) => {
  if (!payload || !Array.isArray(payload.signs) || payload.signs.length === 0) throw new Error("The sign library is empty or unavailable.");
  const ids = new Set();
  payload.signs.forEach((sign, index) => {
    const missing = REQUIRED_SIGN_FIELDS.filter((field) => !(field in sign));
    if (missing.length) throw new Error(`Sign record ${index + 1} is missing: ${missing.join(", ")}.`);
    if (ids.has(sign.id)) throw new Error(`Duplicate sign id: ${sign.id}.`);
    ids.add(sign.id);
    ["routine", "short_family_guidance", "try_it_during", "teacher_message", "family_message"].forEach((field) => {
      if (!sign[field]?.en || !sign[field]?.es) throw new Error(`${sign.id} requires English and Spanish ${field}.`);
    });
  });
  return payload.signs;
};

const selectedSign = () => builder.signs.find((sign) => sign.id === builder.selectedId);
const isEligible = (sign) => Boolean(sign && (sign.flashcard_status === "preview_ready_with_placeholder" || sign.publication_status === "published"));
const signOptionLabel = (sign) => isEligible(sign)
  ? `${sign.display_name} — Internal visual proof available`
  : `${sign.display_name} — Not ready`;

const loadReviewedHandoff = () => {
  if (new URLSearchParams(window.location.search).get("reviewed") !== "1") return null;
  try {
    const payload = JSON.parse(sessionStorage.getItem("kinderflowReviewedContentPack") || "null");
    const bilingual = (value) => value?.en?.trim() && value?.es?.trim();
    if (!payload || payload.review_status !== "APPROVED" || payload.human_review?.approved !== true || !payload.sign_id || !bilingual(payload.family_guidance) || !bilingual(payload.routine_context)) return null;
    return payload;
  } catch (error) {
    return null;
  }
};

const applyReviewedHandoff = () => {
  const handoff = loadReviewedHandoff();
  if (!handoff) return;
  const sign = builder.signs.find((item) => item.sign_id === handoff.sign_id);
  if (!sign) return;
  sign.short_family_guidance = handoff.family_guidance;
  sign.routine = handoff.routine_context;
  builder.reviewedHandoff = handoff;
};

const resetApproval = ({ eligible = true } = {}) => {
  builder.layoutReviewed = false;
  preApprovalActions.hidden = !eligible;
  postApprovalActions.hidden = true;
  reviewButton.disabled = !eligible;
  reviewButton.textContent = "Approve flashcard";
  reviewStateText.textContent = eligible ? "Internal preview" : "Not ready";
  state.textContent = eligible ? "Internal preview" : "Not ready";
  state.className = eligible ? "status-pill status-review" : "status-pill status-fail";
};

const outputFor = (sign) => {
  if (sign.sign_id === "more") return MORE_ROUTINE_COPY[builder.language];
  return {
    routine: sign.routine[builder.language],
    guidance: sign.short_family_guidance[builder.language]
  };
};

const render = () => {
  const sign = selectedSign();
  if (!sign) return;
  const eligible = isEligible(sign);
  resetApproval({ eligible });
  card.hidden = !eligible;
  previewEmpty.hidden = eligible;

  if (!eligible) {
    previewTitle.textContent = `${sign.display_name} · Not ready`;
    previewEmpty.querySelector(".card-label").textContent = "Not ready";
    previewEmpty.querySelector("h3").textContent = "This sign is not ready for Flashcard creation yet.";
    previewEmpty.querySelector("p:not(.card-label)").textContent = "Its visual and hand-pose review must be completed in Master Content Studio first.";
    document.querySelector("#sign-source-help").textContent = `${sign.display_name} does not yet have an eligible visual and hand-pose proof.`;
    status.textContent = "Choose MORE to review the available internal visual proof, or return to Master Content Studio.";
    return;
  }

  const copy = OUTPUT_COPY[builder.language];
  const output = outputFor(sign);
  const word = builder.language === "es" ? sign.spanish_label : sign.display_name;
  card.dataset.cardType = builder.cardType;
  card.querySelector("[data-card-sign]").textContent = word;
  card.querySelector("[data-card-spanish]").textContent = sign.spanish_label;
  card.querySelector('[data-card-label="routine"]').textContent = copy.routine;
  card.querySelector('[data-card-label="guidance"]').textContent = copy.guidance;
  card.querySelector("[data-card-routine]").textContent = output.routine;
  card.querySelector("[data-card-guidance]").textContent = output.guidance;
  card.querySelector("[data-card-kind]").textContent = builder.cardType === "flashcard" ? "FLASHCARD" : "ROUTINE CARD";
  card.querySelector(".flashcard-visual").setAttribute("aria-label", `Internal illustration placeholder for ${word}; final hand pose is not approved`);
  card.setAttribute("aria-label", `Kinder Signs ${builder.cardType === "flashcard" ? "flashcard" : "routine card"} internal preview for ${word}`);
  previewTitle.textContent = `${builder.cardType === "flashcard" ? "Flashcard" : "Routine Card"} · ${copy.language}`;
  document.querySelector("#sign-source-help").textContent = builder.reviewedHandoff?.sign_id === sign.sign_id
    ? `${sign.display_name} uses the locally reviewed Content Pack. Visual and hand-pose approval remain separate.`
    : `${sign.display_name} has an internal visual proof. Final hand and visual review still block publication.`;
  status.textContent = `${copy.language} ${builder.cardType === "flashcard" ? "Flashcard" : "Routine Card"} preview ready. Changes appear immediately.`;
};

const populateSignSelect = () => {
  const eligibleGroup = document.createElement("optgroup");
  eligibleGroup.label = "Eligible for internal proof";
  const unavailableGroup = document.createElement("optgroup");
  unavailableGroup.label = "Not ready";
  builder.signs.forEach((sign) => {
    const option = document.createElement("option");
    option.value = sign.id;
    option.textContent = signOptionLabel(sign);
    (isEligible(sign) ? eligibleGroup : unavailableGroup).append(option);
  });
  signSelect.replaceChildren(eligibleGroup, unavailableGroup);
  const requested = new URLSearchParams(window.location.search).get("sign")?.trim().toUpperCase();
  const requestedSign = builder.signs.find((sign) => sign.display_name === requested);
  builder.selectedId = requestedSign?.id || builder.signs.find(isEligible)?.id || builder.signs[0].id;
  signSelect.value = builder.selectedId;
  signSelect.disabled = builder.signs.length === 0;
};

const loadSigns = async () => {
  try {
    const response = await fetch("data/signs.json", { cache: "no-store" });
    if (!response.ok) throw new Error("The sign library could not be loaded.");
    builder.signs = validateSignData(await response.json());
    applyReviewedHandoff();
    populateSignSelect();
    render();
  } catch (error) {
    signSelect.disabled = true;
    reviewButton.disabled = true;
    preApprovalActions.hidden = true;
    card.hidden = true;
    previewEmpty.hidden = false;
    previewEmpty.querySelector(".card-label").textContent = "Unavailable";
    previewEmpty.querySelector("h3").textContent = "The sign library could not be loaded.";
    previewEmpty.querySelector("p").textContent = "Start the local prototype server and reload this page.";
    status.textContent = `${error.message} Serve the prototype over HTTP and try again.`;
  }
};

signSelect.addEventListener("change", () => { builder.selectedId = signSelect.value; render(); });
document.querySelectorAll('input[name="language"]').forEach((input) => input.addEventListener("change", () => { builder.language = input.value; render(); }));
document.querySelectorAll('input[name="card_type"]').forEach((input) => input.addEventListener("change", () => { builder.cardType = input.value; render(); }));

reviewButton.addEventListener("click", () => {
  const sign = selectedSign();
  if (!isEligible(sign)) return;
  builder.layoutReviewed = true;
  preApprovalActions.hidden = true;
  postApprovalActions.hidden = false;
  state.textContent = "Approved locally";
  state.className = "status-pill status-ready";
  reviewStateText.textContent = "Approved locally";
  printButton.disabled = !sign.printable || typeof window.print !== "function";
  status.textContent = printButton.disabled
    ? "The proof is approved locally, but browser printing is not available."
    : "Local proof approved. Print / Save as PDF is now available; library publication remains blocked.";
});

printButton.addEventListener("click", () => {
  if (!builder.layoutReviewed || printButton.disabled) return;
  status.textContent = "Opening the browser print dialog. Choose Save as PDF to create the proof.";
  window.print();
});

document.querySelector("#create-another").addEventListener("click", () => {
  builder.language = "en";
  builder.cardType = "flashcard";
  document.querySelector('input[name="language"][value="en"]').checked = true;
  document.querySelector('input[name="card_type"][value="flashcard"]').checked = true;
  render();
  signSelect.focus();
});

loadSigns();
