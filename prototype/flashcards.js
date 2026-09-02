"use strict";

const REQUIRED_SIGN_FIELDS = [
  "id", "display_name", "spanish_label", "routine", "short_family_guidance",
  "try_it_during", "publication_status", "school_visibility", "flashcard_status",
  "video_asset", "character_asset", "hand_pose_asset", "movement_reference",
  "school_pack_required", "printable", "image_export_available", "last_reviewed",
  "review_status"
];

const UI_COPY = {
  es: {
    language: "Español", routine: "Rutina", guidance: "Guía para la familia",
    try: "Pruébalo durante…",
    footer: "El vídeo enseña el movimiento. Esta tarjeta refuerza el signo y su rutina."
  },
  en: {
    language: "English", routine: "Routine", guidance: "Family guidance",
    try: "Try it during…",
    footer: "The video teaches the movement. This card reinforces the sign and its routine."
  }
};

const STATUS_LABELS = {
  published: "Published", draft: "Needs review", ready: "Ready",
  needs_artwork: "Needs artwork", needs_review: "Needs review",
  visible: "Visible to schools", hidden: "Not visible", pending: "Pending",
  waiting_for_asset: "Waiting for asset"
};

const builder = { signs: [], selectedId: null, language: "es", cardType: "flashcard", layoutReviewed: false };
const card = document.querySelector(".flashcard-output");
const signSelect = document.querySelector("#published-sign");
const preview = document.querySelector("#builder-preview");
const previewTitle = document.querySelector("#preview-title");
const state = document.querySelector("#flashcard-state");
const status = document.querySelector("#builder-status");
const reviewButton = document.querySelector("#review-flashcard");
const printButton = document.querySelector("#print-flashcard");
const libraryBody = document.querySelector("#flashcard-library-body");

const humanStatus = (value) => STATUS_LABELS[value] || value.replaceAll("_", " ").replace(/^./, (letter) => letter.toUpperCase());

const validateSignData = (payload) => {
  if (!payload || !Array.isArray(payload.signs) || payload.signs.length === 0) throw new Error("The sign library is empty or unavailable.");
  const ids = new Set();
  payload.signs.forEach((sign, index) => {
    const missing = REQUIRED_SIGN_FIELDS.filter((field) => !(field in sign));
    if (missing.length) throw new Error(`Sign record ${index + 1} is missing: ${missing.join(", ")}.`);
    if (ids.has(sign.id)) throw new Error(`Duplicate sign id: ${sign.id}.`);
    ids.add(sign.id);
    ["routine", "short_family_guidance", "try_it_during"].forEach((field) => {
      if (!sign[field]?.en || !sign[field]?.es) throw new Error(`${sign.id} requires English and Spanish ${field}.`);
    });
  });
  return payload.signs;
};

const selectedSign = () => builder.signs.find((sign) => sign.id === builder.selectedId);

const resetLayoutReview = () => {
  builder.layoutReviewed = false;
  reviewButton.disabled = false;
  reviewButton.textContent = "Mark layout reviewed";
  printButton.disabled = true;
  state.textContent = "Needs artwork";
  state.className = "status-pill status-review";
  status.textContent = "Layout draft ready. Final illustration and hand-pose review are still required.";
};

const renderLibrary = () => {
  libraryBody.replaceChildren(...builder.signs.map((sign) => {
    const row = document.createElement("tr");
    const values = [sign.display_name, sign.routine.en, humanStatus(sign.video_asset), humanStatus(sign.flashcard_status), humanStatus(sign.publication_status), humanStatus(sign.school_visibility)];
    values.forEach((value, index) => {
      const cell = document.createElement(index === 0 ? "th" : "td");
      if (index === 0) cell.scope = "row";
      cell.textContent = value;
      row.append(cell);
    });
    const previewCell = document.createElement("td");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "text-link-button";
    button.dataset.previewSign = sign.id;
    button.textContent = sign.publication_status === "published" ? "Preview" : "View status";
    previewCell.append(button);
    row.append(previewCell);
    return row;
  }));
};

const render = ({ preserveReview = false } = {}) => {
  const sign = selectedSign();
  if (!sign) return;
  const copy = UI_COPY[builder.language];
  card.dataset.cardType = builder.cardType;
  card.querySelector("[data-card-sign]").textContent = sign.display_name;
  card.querySelector("[data-card-spanish]").textContent = sign.spanish_label;
  card.querySelector('[data-card-label="routine"]').textContent = copy.routine;
  card.querySelector('[data-card-label="guidance"]').textContent = copy.guidance;
  card.querySelector('[data-card-label="try"]').textContent = copy.try;
  card.querySelector("[data-card-routine]").textContent = sign.routine[builder.language];
  card.querySelector("[data-card-guidance]").textContent = sign.short_family_guidance[builder.language];
  card.querySelector("[data-card-try]").textContent = sign.try_it_during[builder.language];
  card.querySelector("[data-card-footer]").textContent = copy.footer;
  card.querySelector("[data-card-kind]").textContent = builder.cardType === "flashcard" ? "FLASHCARD" : "ROUTINE CARD";
  card.querySelector(".flashcard-visual").setAttribute("aria-label", `${sign.display_name} illustration asset pending`);
  previewTitle.textContent = `${builder.cardType === "flashcard" ? "Flashcard" : "Routine card"} · ${copy.language}`;
  document.querySelector("#source-description").textContent = sign.short_family_guidance.en;
  document.querySelector("#illustration-status").textContent = humanStatus(sign.illustration_status);
  document.querySelector("#hand-pose-status").textContent = humanStatus(sign.hand_pose_asset);
  document.querySelector("#print-readiness").textContent = sign.printable ? "Proof available" : "Not ready";
  document.querySelector("#sign-source-help").textContent = sign.publication_status === "published"
    ? `${sign.display_name} is a published source item. Artwork status remains separate.`
    : `${sign.display_name} is visible for readiness review but cannot be used for a production flashcard yet.`;
  if (!preserveReview) resetLayoutReview();
};

const populateSignSelect = () => {
  signSelect.replaceChildren(...builder.signs.map((sign) => {
    const option = document.createElement("option");
    option.value = sign.id;
    option.textContent = `${sign.display_name} · ${humanStatus(sign.publication_status)}`;
    option.disabled = sign.publication_status !== "published";
    return option;
  }));
  const requested = new URLSearchParams(window.location.search).get("sign")?.trim().toUpperCase();
  const published = builder.signs.filter((sign) => sign.publication_status === "published");
  const requestedSign = published.find((sign) => sign.display_name === requested);
  builder.selectedId = requestedSign?.id || published[0]?.id || builder.signs[0].id;
  signSelect.value = builder.selectedId;
  signSelect.disabled = published.length === 0;
};

const loadSigns = async () => {
  try {
    const response = await fetch("data/signs.json", { cache: "no-store" });
    if (!response.ok) throw new Error("The sign library could not be loaded.");
    builder.signs = validateSignData(await response.json());
    populateSignSelect();
    renderLibrary();
    render();
  } catch (error) {
    signSelect.disabled = true;
    reviewButton.disabled = true;
    status.textContent = `${error.message} Serve the prototype over HTTP to use the data-driven Studio.`;
    libraryBody.innerHTML = '<tr><td colspan="7">Sign data unavailable. Start the local prototype server and reload.</td></tr>';
  }
};

signSelect.addEventListener("change", () => { builder.selectedId = signSelect.value; render(); });
document.querySelectorAll('input[name="language"]').forEach((input) => input.addEventListener("change", () => { builder.language = input.value; render(); }));
document.querySelectorAll('input[name="card_type"]').forEach((input) => input.addEventListener("change", () => { builder.cardType = input.value; render(); }));

document.querySelector("#preview-card").addEventListener("click", () => {
  preview.scrollIntoView({ behavior: "smooth", block: "start" });
  preview.focus({ preventScroll: true });
});

reviewButton.addEventListener("click", () => {
  const sign = selectedSign();
  builder.layoutReviewed = true;
  state.textContent = "Artwork pending";
  state.className = "status-pill status-review";
  reviewButton.disabled = true;
  reviewButton.textContent = "Layout reviewed";
  printButton.disabled = !sign.printable;
  status.textContent = sign.printable
    ? "Layout review recorded locally. A marked browser print proof is available."
    : "Layout review recorded locally. Printing remains unavailable until the source item is ready.";
});

printButton.addEventListener("click", () => {
  if (!builder.layoutReviewed || printButton.disabled) return;
  status.textContent = "Opening the browser print dialog. Choose Save as PDF for a review proof.";
  window.print();
});

libraryBody.addEventListener("click", (event) => {
  const button = event.target.closest("[data-preview-sign]");
  if (!button) return;
  const sign = builder.signs.find((item) => item.id === button.dataset.previewSign);
  if (sign.publication_status === "published") {
    builder.selectedId = sign.id;
    signSelect.value = sign.id;
    render();
    preview.scrollIntoView({ behavior: "smooth", block: "start" });
  } else {
    status.textContent = `${sign.display_name} needs review and is not available as a flashcard source yet.`;
    document.querySelector("#flashcard-library-title").scrollIntoView({ behavior: "smooth", block: "start" });
  }
});

loadSigns();
