"use strict";

const contentPackSign = document.querySelector("#content-pack-sign");
const contentPackLanguage = document.querySelector("#content-pack-language");
const generateContentPack = document.querySelector("#generate-content-pack");
const approveContentPack = document.querySelector("#approve-content-pack");
const requestContentChanges = document.querySelector("#request-content-changes");
const restoreHumanCopy = document.querySelector("#restore-human-copy");
const openReviewedFlashcard = document.querySelector("#open-reviewed-flashcard");
const openSchoolPreview = document.querySelector("#open-school-preview");
const openFamilyPreview = document.querySelector("#open-family-preview");
const contentPackJson = document.querySelector("#content-pack-json");
const contentGateResults = document.querySelector("#content-gate-results");
const contentEngineStatus = document.querySelector("#content-engine-status");
const contentOutputState = document.querySelector("#content-output-state");

let contentEngineRecords = [];
let activeRun = null;
let backendAvailable = false;
let requestedRoutineContext = "";

const DISPLAY_LABELS = {
  technical_evidence_available: "Reference movement available",
  needs_reference_review: "Reference needs review",
  controlled_vector_proof_ready: "Illustration ready for review",
  candidates_ready_for_founder_review: "Illustration options need review",
  context_asset_ready: "Everyday context ready",
  manual_export_identified: "Everyday context optional",
  ready_for_human_review: "Ready for human review",
  BLOCKED_BY_HAND_REVIEW: "Complete visual review first",
  BLOCKED: "Not ready",
  llm_assisted: "AI-assisted draft",
  human: "Approved source copy",
  DRY_RUN: "Demo mode",
  DRY_RUN_ONLY: "Demo check only",
  NOT_APPLICABLE: "Not used for this step",
  READY_FOR_REVIEW: "Ready for review",
  APPROVED_LOCALLY: "Approved locally",
  CHANGES_REQUESTED: "Changes requested",
  PENDING: "Pending"
};
const friendlyState = (value) => DISPLAY_LABELS[value] || String(value || "—").replaceAll("_", " ").toLowerCase().replace(/^./, (letter) => letter.toUpperCase());
const setEngineText = (selector, value) => { document.querySelector(selector).textContent = value; };
const selectedEngineRecord = () => contentEngineRecords.find((item) => item.sign_id === contentPackSign.value);
const selectedOrigin = () => document.querySelector('input[name="content_origin"]:checked').value;
const normalizeRequestedSign = (value) => String(value || "")
  .trim()
  .toLowerCase()
  .replaceAll(/[^a-z0-9]+/g, "_")
  .replaceAll(/^_+|_+$/g, "");
const requestedSignLabel = (signId) => signId
  ? signId.replaceAll("_", " ").toUpperCase()
  : "REQUESTED SIGN";
const ROUTINE_TRANSLATIONS = new Map([
  ["snack time", "Hora de la merienda"],
  ["playtime", "Hora de jugar"],
  ["mealtime", "Hora de comer"],
  ["bedtime", "Hora de dormir"],
  ["getting ready", "Prepararse"],
  ["milk time", "Hora de la leche"],
  ["drink break", "Pausa para beber"]
]);
const routineForLanguage = (value, language) => {
  const routine = String(value || "").trim();
  if (!routine || language === "en") return routine;
  return routine.split(/(\s*[,/]\s*)/).map((part) => {
    if (/^[\s,\/]+$/.test(part)) return part;
    return ROUTINE_TRANSLATIONS.get(part.trim().toLowerCase()) || part.trim();
  }).join("");
};
const resolvedRoutine = (record) => requestedRoutineContext
  ? { en: requestedRoutineContext, es: routineForLanguage(requestedRoutineContext, "es") }
  : structuredClone(record.input.routine);

const setOutputState = (label, tone = "neutral") => {
  contentOutputState.textContent = label;
  contentOutputState.className = `status-pill status-${tone}`;
};

const setLinkState = (link, enabled, href) => {
  link.classList.toggle("is-disabled", !enabled);
  link.setAttribute("aria-disabled", String(!enabled));
  link.href = enabled ? href : link.dataset.fallbackHref;
};

[openReviewedFlashcard, openSchoolPreview, openFamilyPreview].forEach((link) => {
  link.dataset.fallbackHref = link.getAttribute("href");
  link.addEventListener("click", (event) => {
    if (link.getAttribute("aria-disabled") === "true") event.preventDefault();
  });
});

const lockReviewedHandoffs = () => {
  setLinkState(openReviewedFlashcard, false, "flashcards.html");
  openReviewedFlashcard.textContent = "Create flashcard";
  setLinkState(openSchoolPreview, false, "school.html");
  setLinkState(openFamilyPreview, false, "family.html");
};

const resetCandidate = () => {
  activeRun = null;
  contentPackJson.textContent = "No Content Pack generated.";
  contentGateResults.innerHTML = "<li>Waiting for structured output.</li>";
  approveContentPack.disabled = true;
  requestContentChanges.disabled = true;
  restoreHumanCopy.disabled = true;
  approveContentPack.textContent = "Approve content";
  setOutputState("Waiting");
  setEngineText("#engine-ai", "Not generated");
  setEngineText("#engine-gate", "Waiting");
  setEngineText("#engine-langsmith", "Waiting");
  setEngineText("#engine-review", "Pending");
  setEngineText("#engine-flashcard", "Blocked");
  lockReviewedHandoffs();
};

const clearUnsupportedSignOption = () => {
  contentPackSign.querySelector('option[data-unsupported-sign="true"]')?.remove();
  contentPackSign.removeAttribute("aria-invalid");
};

const renderUnsupportedSign = (signId) => {
  const label = requestedSignLabel(signId);
  resetCandidate();
  setEngineText("#content-source-title", `${label} is not available`);
  setEngineText("#content-source-copy", "Choose another sign to prepare family wording.");
  setEngineText("#engine-movement", "Not available");
  setEngineText("#engine-character", "Not available");
  setEngineText("#engine-context", "Not available");
  setEngineText("#engine-hand", "Not available");
  setEngineText("#engine-library", "Not available");
  contentEngineStatus.textContent = "This sign is not available in the current demo set. Choose another sign.";
  setOutputState("Not available", "review");
  generateContentPack.disabled = true;
  contentPackSign.setAttribute("aria-invalid", "true");
};

const selectUnsupportedSign = (signId) => {
  clearUnsupportedSignOption();
  const option = document.createElement("option");
  option.value = signId;
  option.textContent = `${requestedSignLabel(signId)} — Not available`;
  option.dataset.unsupportedSign = "true";
  contentPackSign.append(option);
  contentPackSign.value = signId;
};

const sourceForLanguage = (record) => ({
  ...structuredClone(record.input),
  routine: resolvedRoutine(record),
  language: contentPackLanguage.value
});

const renderSource = () => {
  const record = selectedEngineRecord();
  if (!record) {
    renderUnsupportedSign(contentPackSign.value);
    return;
  }
  clearUnsupportedSignOption();
  generateContentPack.disabled = false;
  const source = sourceForLanguage(record);
  setEngineText("#content-source-title", `${source.display_name} / ${source.spanish_label} · ${source.routine[contentPackLanguage.value]}`);
  setEngineText("#content-source-copy", `${source.approved_context.school_use.en} ${source.approved_context.family_use.en}`);
  setEngineText("#engine-movement", friendlyState(record.readiness.movement_intelligence));
  setEngineText("#engine-character", friendlyState(record.readiness.character));
  setEngineText("#engine-context", friendlyState(record.readiness.context));
  setEngineText("#engine-hand", friendlyState(record.readiness.hand_pose));
  setEngineText("#engine-library", friendlyState(record.readiness.library));
  contentEngineStatus.textContent = `${source.display_name} wording source loaded. Existing approved copy is unchanged.`;
  resetCandidate();
};

const renderGate = (gate) => {
  const items = gate?.passed
    ? ["Structured JSON is valid.", "Required outputs are present and within length limits.", "Labels and source identifiers are preserved.", "No biomechanics, correctness claims or unsupported clinical/developmental claims were detected.", "Human review and no-auto-publication controls are preserved."]
    : gate?.blocking_reasons || ["No quality-gate result is available."];
  contentGateResults.replaceChildren(...items.map((message) => {
    const item = document.createElement("li");
    item.textContent = message;
    return item;
  }));
};

const renderRun = (run, sourceLabel = "Local backend") => {
  activeRun = run;
  contentPackJson.textContent = JSON.stringify(run.content_pack || run.error || {}, null, 2);
  renderGate(run.quality_gate);
  const passed = run.quality_gate?.passed === true;
  const rejected = run.state === "REJECTED" || run.state === "FAILED";
  setOutputState(rejected ? "Rejected safely" : run.state === "APPROVED_LOCALLY" ? "Approved locally" : "Ready for review", rejected ? "review" : run.state === "APPROVED_LOCALLY" ? "ready" : "review");
  setEngineText("#engine-ai", `${friendlyState(run.generation.method)} · ${friendlyState(run.generation.mode)}`);
  setEngineText("#engine-gate", passed ? "Pass" : "Fail");
  setEngineText("#engine-langsmith", `${friendlyState(run.langsmith.mode)} · ${friendlyState(run.langsmith.evaluation_status)}`);
  setEngineText("#engine-review", run.review?.status === "APPROVED" ? "Approved · local" : friendlyState(run.review?.status || "PENDING"));
  setEngineText("#engine-flashcard", run.flashcard_handoff ? "Preview ready" : "Blocked until content approval");
  approveContentPack.disabled = !passed || run.state !== "READY_FOR_REVIEW";
  requestContentChanges.disabled = !["READY_FOR_REVIEW", "APPROVED_LOCALLY"].includes(run.state);
  restoreHumanCopy.disabled = run.generation.method !== "llm_assisted";
  const reviewed = run.review?.status === "APPROVED" && run.content_pack?.human_review?.approved === true;
  if (reviewed) {
    sessionStorage.setItem("kinderflowReviewedContentPack", JSON.stringify(run.content_pack));
    const sign = encodeURIComponent(run.content_pack.flashcard_copy.primary_label);
    setLinkState(openReviewedFlashcard, false, "flashcards.html");
    openReviewedFlashcard.textContent = "Approve a visual to create printable";
    setLinkState(openSchoolPreview, true, `school.html?sign=${sign}&reviewed=1`);
    setLinkState(openFamilyPreview, true, `family.html?sign=${sign}&reviewed=1`);
  } else {
    lockReviewedHandoffs();
  }
  const draftSource = friendlyState(run.generation.method);
  contentEngineStatus.textContent = `${draftSource}: ${friendlyState(run.state)}. Nothing was added to the library.`;
};

const staticFallbackRun = () => {
  const record = selectedEngineRecord();
  const origin = selectedOrigin();
  const candidate = structuredClone(record.candidate_output);
  candidate.routine_context = resolvedRoutine(record);
  candidate.generation_method = origin;
  candidate.generation_mode = origin === "llm_assisted" ? "DRY_RUN" : "NOT_APPLICABLE";
  candidate.language = contentPackLanguage.value;
  return {
    run_id: candidate.run_id,
    state: "READY_FOR_REVIEW",
    generation: { method: origin, mode: candidate.generation_mode, latency_ms: 0 },
    content_pack: candidate,
    quality_gate: record.deterministic_quality_gate,
    langsmith: origin === "human"
      ? { mode: "NOT_APPLICABLE", evaluation_status: "NOT_APPLICABLE" }
      : { mode: "DRY_RUN", evaluation_status: "DRY_RUN_ONLY" },
    review: { status: "PENDING" },
    flashcard_handoff: null
  };
};

const callContentApi = async (path, options = {}) => {
  const response = await fetch(path, { cache: "no-store", ...options, headers: { "Content-Type": "application/json", ...(options.headers || {}) } });
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) throw new Error("LOCAL_BACKEND_UNAVAILABLE");
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "The family content request failed.");
  return payload;
};

generateContentPack.addEventListener("click", async () => {
  const record = selectedEngineRecord();
  if (!record) return;
  generateContentPack.disabled = true;
  contentEngineStatus.textContent = "Preparing family content…";
  setOutputState("Running", "review");
  try {
    if (!backendAvailable) throw new Error("LOCAL_BACKEND_UNAVAILABLE");
    const run = await callContentApi("/api/content-packs/generate", {
      method: "POST",
      body: JSON.stringify({ operation: "GENERATE_CONTENT_PACK", generation_method: selectedOrigin(), input: sourceForLanguage(record) })
    });
    renderRun(run);
  } catch (error) {
    if (error.message === "LOCAL_BACKEND_UNAVAILABLE") {
      renderRun(staticFallbackRun(), "Static fallback");
      contentEngineStatus.textContent = "A saved demo draft is ready for human review.";
    } else {
      activeRun = null;
      setOutputState("Failed", "review");
      contentPackJson.textContent = JSON.stringify({ error: error.message }, null, 2);
      contentGateResults.innerHTML = "<li>Generation stopped before human review.</li>";
      contentEngineStatus.textContent = "Family content could not be prepared. Check the technical details or try again.";
    }
  } finally {
    generateContentPack.disabled = false;
  }
});

approveContentPack.addEventListener("click", async () => {
  if (!activeRun?.quality_gate?.passed) return;
  try {
    let reviewed;
    if (backendAvailable && activeRun.run_id.startsWith("content_")) {
      reviewed = await callContentApi(`/api/content-packs/${encodeURIComponent(activeRun.run_id)}/approve`, { method: "POST", body: "{}" });
    } else {
      reviewed = structuredClone(activeRun);
      reviewed.state = "APPROVED_LOCALLY";
      reviewed.content_pack.review_status = "APPROVED";
      reviewed.content_pack.human_review = { mode: "LOCAL_DEMO", approved: true, actor_type: "human_reviewer" };
      reviewed.review = { status: "APPROVED", actor_type: "human_reviewer" };
      reviewed.flashcard_handoff = { sign_id: reviewed.content_pack.sign_id };
    }
    renderRun(reviewed, backendAvailable ? "Local backend" : "Static fallback");
  } catch (error) {
    contentEngineStatus.textContent = error.message;
  }
});

requestContentChanges.addEventListener("click", async () => {
  if (!activeRun) return;
  try {
    if (backendAvailable) activeRun = await callContentApi(`/api/content-packs/${encodeURIComponent(activeRun.run_id)}/request-changes`, { method: "POST", body: "{}" });
    else {
      activeRun.state = "CHANGES_REQUESTED";
      activeRun.review = { status: "CHANGES_REQUESTED", actor_type: "human_reviewer" };
      activeRun.flashcard_handoff = null;
    }
    sessionStorage.removeItem("kinderflowReviewedContentPack");
    renderRun(activeRun, backendAvailable ? "Local backend" : "Static fallback");
  } catch (error) {
    contentEngineStatus.textContent = error.message;
  }
});

restoreHumanCopy.addEventListener("click", async () => {
  if (!activeRun) return;
  try {
    const restored = backendAvailable
      ? await callContentApi(`/api/content-packs/${encodeURIComponent(activeRun.run_id)}/restore`, { method: "POST", body: "{}" })
      : (() => { document.querySelector('input[name="content_origin"][value="human"]').checked = true; return staticFallbackRun(); })();
    renderRun(restored, backendAvailable ? "Local backend" : "Static fallback");
    contentEngineStatus.textContent = "Approved source copy restored as a separate draft for review. The earlier draft was kept.";
  } catch (error) {
    contentEngineStatus.textContent = error.message;
  }
});

contentPackSign.addEventListener("change", renderSource);
contentPackLanguage.addEventListener("change", resetCandidate);
document.querySelectorAll('input[name="content_origin"]').forEach((input) => input.addEventListener("change", resetCandidate));

const checkBackend = async () => {
  try {
    const response = await fetch("/api/health", { cache: "no-store" });
    const health = await response.json();
    backendAvailable = response.ok && health.capabilities?.includes("generate_content_pack");
  } catch (_error) {
    backendAvailable = false;
  }
  setEngineText("#engine-backend", backendAvailable ? "Connected" : "Saved demo available");
};

const loadContentEngine = async () => {
  try {
    await checkBackend();
    const response = await fetch("data/content_engine_demo.json", { cache: "no-store" });
    if (!response.ok) throw new Error("Family content data is unavailable.");
    const report = await response.json();
    if (report.operation !== "GENERATE_CONTENT_PACK" || !Array.isArray(report.results) || report.results.length !== 5) throw new Error("Family content data could not be read.");
    contentEngineRecords = report.results;
    const parameters = new URLSearchParams(window.location.search);
    requestedRoutineContext = (parameters.get("routine") || "").trim().slice(0, 180);
    if (parameters.has("sign")) {
      const requested = normalizeRequestedSign(parameters.get("sign"));
      if (contentEngineRecords.some((item) => item.sign_id === requested)) contentPackSign.value = requested;
      else selectUnsupportedSign(requested);
    }
    renderSource();
  } catch (error) {
    generateContentPack.disabled = true;
    contentEngineStatus.textContent = `${error.message} Reload the page after the local content service is ready.`;
  }
};

loadContentEngine();
