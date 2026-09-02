"use strict";

const contentPackSign = document.querySelector("#content-pack-sign");
const generateContentPack = document.querySelector("#generate-content-pack");
const approveContentPack = document.querySelector("#approve-content-pack");
const openReviewedFlashcard = document.querySelector("#open-reviewed-flashcard");
const contentPackJson = document.querySelector("#content-pack-json");
const contentGateResults = document.querySelector("#content-gate-results");
const contentEngineStatus = document.querySelector("#content-engine-status");
const contentOutputState = document.querySelector("#content-output-state");

let contentEngineRecords = [];
let activeCandidate = null;
let activeGate = null;

const friendlyState = (value) => String(value || "—").replaceAll("_", " ").toLowerCase().replace(/^./, (letter) => letter.toUpperCase());
const setEngineText = (selector, value) => { document.querySelector(selector).textContent = value; };
const selectedEngineRecord = () => contentEngineRecords.find((item) => item.sign_id === contentPackSign.value);

const setOutputState = (label, tone = "neutral") => {
  contentOutputState.textContent = label;
  contentOutputState.className = `status-pill status-${tone}`;
};

const lockFlashcardHandoff = () => {
  openReviewedFlashcard.classList.add("is-disabled");
  openReviewedFlashcard.setAttribute("aria-disabled", "true");
  openReviewedFlashcard.href = "flashcards.html";
};

const resetCandidate = () => {
  activeCandidate = null;
  activeGate = null;
  contentPackJson.textContent = "No Content Pack generated.";
  contentGateResults.innerHTML = "<li>Waiting for structured output.</li>";
  approveContentPack.disabled = true;
  approveContentPack.textContent = "Approve Content";
  setOutputState("Waiting");
  setEngineText("#engine-ai", "Not generated");
  setEngineText("#engine-gate", "Waiting");
  setEngineText("#engine-langsmith", "Waiting");
  setEngineText("#engine-review", "Pending");
  setEngineText("#engine-flashcard", "Blocked");
  lockFlashcardHandoff();
};

const renderSource = () => {
  const record = selectedEngineRecord();
  if (!record) return;
  const source = record.input;
  setEngineText("#content-source-title", `${source.display_name} / ${source.spanish_label} · ${source.routine.en}`);
  setEngineText("#content-source-copy", source.approved_context.school_use.en);
  setEngineText("#engine-movement", friendlyState(record.readiness.movement_intelligence));
  setEngineText("#engine-character", friendlyState(record.readiness.character));
  setEngineText("#engine-context", friendlyState(record.readiness.context));
  setEngineText("#engine-hand", friendlyState(record.readiness.hand_pose));
  setEngineText("#engine-library", friendlyState(record.readiness.library));
  setEngineText("#engine-langsmith", "Waiting");
  contentEngineStatus.textContent = `${source.display_name} source context loaded. Generate explicitly; existing human copy is unchanged.`;
  resetCandidate();
};

const renderGate = (gate) => {
  const items = gate.passed
    ? ["Structured JSON is valid.", "Required outputs are present.", "Labels and source identifiers are preserved.", "No biomechanics or unsupported claims detected.", "Human review and no-auto-publication controls are preserved."]
    : gate.blocking_reasons;
  contentGateResults.replaceChildren(...items.map((message) => {
    const item = document.createElement("li");
    item.textContent = message;
    return item;
  }));
};

const selectedOrigin = () => document.querySelector('input[name="content_origin"]:checked').value;

generateContentPack.addEventListener("click", () => {
  const record = selectedEngineRecord();
  if (!record) return;
  const origin = selectedOrigin();
  activeCandidate = structuredClone(record.candidate_output);
  activeCandidate.generation_method = origin;
  activeCandidate.generation_mode = origin === "llm_assisted" ? "DRY_RUN" : "NOT_APPLICABLE";
  activeGate = record.deterministic_quality_gate;
  contentPackJson.textContent = JSON.stringify(activeCandidate, null, 2);
  renderGate(activeGate);
  setOutputState(activeGate.passed ? "Ready for review" : "Rejected", activeGate.passed ? "review" : "review");
  setEngineText("#engine-ai", origin === "llm_assisted" ? "AI-assisted draft" : "Human-written source");
  setEngineText("#engine-gate", activeGate.passed ? "Pass" : "Fail");
  setEngineText("#engine-langsmith", origin === "llm_assisted" ? "Dry-run · not sent" : "Not applicable");
  approveContentPack.disabled = !activeGate.passed;
  contentEngineStatus.textContent = origin === "llm_assisted"
    ? "Dry-run candidate created from the structured source. No live LLM or LangSmith trace was called."
    : "Human-written source packaged without LLM use. LangSmith is not applicable.";
});

approveContentPack.addEventListener("click", () => {
  if (!activeCandidate || !activeGate?.passed) return;
  const reviewed = structuredClone(activeCandidate);
  reviewed.review_status = "APPROVED";
  reviewed.human_review = { mode: "LOCAL_DEMO", approved: true };
  reviewed.automatic_publication = false;
  try {
    sessionStorage.setItem("kinderflowReviewedContentPack", JSON.stringify(reviewed));
  } catch (error) {
    contentEngineStatus.textContent = "Content was reviewed locally, but this browser could not prepare the Flashcard Studio handoff.";
    return;
  }
  contentPackJson.textContent = JSON.stringify(reviewed, null, 2);
  setOutputState("Content approved locally", "ready");
  setEngineText("#engine-review", "Approved · local demo");
  setEngineText("#engine-flashcard", "Preview ready");
  approveContentPack.disabled = true;
  approveContentPack.textContent = "Content approved";
  openReviewedFlashcard.classList.remove("is-disabled");
  openReviewedFlashcard.removeAttribute("aria-disabled");
  openReviewedFlashcard.href = `flashcards.html?sign=${encodeURIComponent(activeCandidate.flashcard_copy.primary_label)}&reviewed=1`;
  contentEngineStatus.textContent = "Reviewed wording is ready for Flashcard Studio. Visual and hand-pose blockers remain separate.";
});

openReviewedFlashcard.addEventListener("click", (event) => {
  if (openReviewedFlashcard.getAttribute("aria-disabled") === "true") event.preventDefault();
});

contentPackSign.addEventListener("change", renderSource);
document.querySelectorAll('input[name="content_origin"]').forEach((input) => input.addEventListener("change", resetCandidate));

const loadContentEngine = async () => {
  try {
    const response = await fetch("data/content_engine_demo.json", { cache: "no-store" });
    if (!response.ok) throw new Error("Content Pack data is unavailable.");
    const report = await response.json();
    if (report.operation !== "GENERATE_CONTENT_PACK" || !Array.isArray(report.results) || report.results.length !== 5) throw new Error("Content Pack contract is invalid.");
    contentEngineRecords = report.results;
    renderSource();
  } catch (error) {
    generateContentPack.disabled = true;
    contentEngineStatus.textContent = `${error.message} Run python -m content_ops and reload.`;
  }
};

loadContentEngine();
