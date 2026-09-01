"use strict";

const OUTPUT_COPY = {
  en: {
    language: "English",
    signLabel: "Sign",
    signName: "MORE",
    routineLabel: "Routine",
    routine: "Snack time · Playtime · Mealtime",
    guidanceLabel: "When and how to use it",
    guidance: "Use the sign naturally when offering or asking for more. Say the word while showing the sign.",
    visual: "Published sign visual"
  },
  es: {
    language: "Spanish",
    signLabel: "Signo",
    signName: "MÁS",
    routineLabel: "Rutina",
    routine: "Merienda · Juego · Comida",
    guidanceLabel: "Cuándo y cómo usarlo",
    guidance: "Usa el signo de forma natural al ofrecer o pedir más. Di la palabra mientras muestras el signo.",
    visual: "Visual del signo publicado"
  }
};

const incoming = new URLSearchParams(window.location.search);
const incomingSign = incoming.get("sign");
const incomingRoutine = incoming.get("routine");
const incomingRun = incoming.get("source_run");
if (incomingSign) {
  const sign = incomingSign.trim().toUpperCase();
  OUTPUT_COPY.en.signName = sign;
  OUTPUT_COPY.es.signName = sign === "MORE" ? "MÁS" : sign;
  if (incomingRoutine && sign !== "MORE") {
    OUTPUT_COPY.en.routine = incomingRoutine;
    OUTPUT_COPY.es.routine = incomingRoutine;
  }
  const signOption = document.querySelector("#published-sign option");
  if (signOption) signOption.textContent = `${sign} · Demo-published sign`;
  const sourceDescription = document.querySelector(".source-description p");
  if (sourceDescription) {
    sourceDescription.textContent = incomingRun
      ? `Loaded from local Create a Sign run ${incomingRun}. Review all language copy before approval.`
      : "Loaded from a demo-published sign. Review all language copy before approval.";
  }
}

const builder = { language: "en", cardType: "flashcard", outputFormat: "pdf", approved: false };
const card = document.querySelector(".flashcard-output");
const preview = document.querySelector("#builder-preview");
const previewTitle = document.querySelector("#preview-title");
const state = document.querySelector("#flashcard-state");
const status = document.querySelector("#builder-status");
const outputHelp = document.querySelector("#output-help");
const approveButton = document.querySelector("#approve-flashcard");
const exportButton = document.querySelector("#export-flashcard");
const markDraft = () => {
  builder.approved = false;
  state.textContent = "Draft";
  state.className = "status-pill status-review";
  approveButton.disabled = false;
  approveButton.textContent = "Approve asset";
  exportButton.disabled = true;
  status.textContent = "Draft updated. Human approval is required before export.";
};

const render = ({ preserveApproval = false } = {}) => {
  const copy = OUTPUT_COPY[builder.language];
  card.dataset.cardType = builder.cardType;
  card.querySelectorAll("[data-card-sign]").forEach((element) => { element.textContent = copy.signName; });
  card.querySelector('[data-card-label="sign"]').textContent = copy.signLabel;
  card.querySelector('[data-card-label="routine"]').textContent = copy.routineLabel;
  card.querySelector('[data-card-label="how"]').textContent = copy.guidanceLabel;
  card.querySelector('[data-card-label="visual"]').textContent = copy.visual;
  card.querySelector("[data-card-routine]").textContent = copy.routine;
  card.querySelector("[data-card-guidance]").textContent = copy.guidance;
  card.querySelector("[data-card-kind]").textContent = builder.cardType === "flashcard" ? "FLASHCARD" : "ROUTINE CARD";
  card.querySelector('[data-card-section="routine"]').hidden = builder.cardType === "flashcard";
  card.querySelector('[data-card-section="guidance"]').hidden = builder.cardType === "flashcard";
  previewTitle.textContent = `${builder.cardType === "flashcard" ? "Flashcard" : "Routine card"} · ${copy.language}`;
  exportButton.textContent = builder.outputFormat === "pdf" ? "Print / Save as PDF" : "Export image";
  outputHelp.textContent = builder.outputFormat === "pdf"
    ? "PDF output uses the browser print dialog. Choose “Save as PDF” to export the reviewed card."
    : "Image export is represented as a prototype action; no image file is generated.";
  if (!preserveApproval) markDraft();
};

document.querySelectorAll('input[name="language"]').forEach((input) => input.addEventListener("change", () => {
  builder.language = input.value;
  render();
}));

document.querySelectorAll('input[name="card_type"]').forEach((input) => input.addEventListener("change", () => {
  builder.cardType = input.value;
  render();
}));

document.querySelectorAll('input[name="output_format"]').forEach((input) => input.addEventListener("change", () => {
  builder.outputFormat = input.value;
  render();
}));

document.querySelector("#preview-card").addEventListener("click", () => {
  preview.scrollIntoView({ behavior: "smooth", block: "start" });
  preview.focus({ preventScroll: true });
});

approveButton.addEventListener("click", () => {
  builder.approved = true;
  state.textContent = "Published asset";
  state.className = "status-pill status-ready";
  approveButton.disabled = true;
  approveButton.textContent = "Approved";
  exportButton.disabled = false;
  status.textContent = "Human approval recorded locally. Export is available for this prototype asset.";
});

exportButton.addEventListener("click", () => {
  if (!builder.approved) return;
  if (builder.outputFormat === "pdf") {
    status.textContent = "Opening the browser print dialog. Choose “Save as PDF” to export.";
    window.print();
  } else {
    status.textContent = "Image export is illustrative in this static prototype; no file was generated.";
  }
});

render({ preserveApproval: true });
