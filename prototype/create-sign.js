"use strict";

const STAGES = [
  ["video_received", "Reference received"],
  ["video_validation", "Check the video"],
  ["landmark_extraction", "Find the reference poses"],
  ["movement_normalization", "Organise the poses"],
  ["motion_analysis", "Find clear moments"],
  ["technical_checks", "Run quality checks"],
  ["results_ready", "Ready to review"]
];
const STAGE_LABELS = Object.fromEntries(STAGES);
const INTERNAL_REFERENCE_STATUS = "Validated reference";
const TRACKED_POSE_MINIMUM_PERCENT = 90;

const SUPPORTED_SIGN_IDS = new Set(["more", "help", "eat", "sleep", "milk", "water"]);

const TECHNICAL_STATUS_COPY = {
  "Pass": { label: "Ready to continue", explanation: "The reference is clear enough to continue." },
  "Review needed": { label: "Review recommended", explanation: "A few moments are worth checking before continuing." },
  "Fail": { label: "Choose another reference", explanation: "There is not enough clear information to continue with this video." }
};

const RUN_STATE_COPY = {
  queued: "Waiting to start",
  processing: "Reference review in progress",
  complete: "Ready to review",
  failed: "Reference review stopped",
  insufficient_coverage: "Choose another reference"
};

const state = {
  inputMode: "upload",
  source: null,
  file: null,
  run: null,
  polling: null,
  submissionPending: false,
  runGeneration: 0,
  visualPackages: [],
  activePackage: null,
  selectedCandidate: null,
  currentCandidates: [],
  evidenceRoute: null,
  selectedFrames: [],
  workflowRecord: null,
  illustrativeCatalog: {}
};
const form = document.querySelector("#sign-run-form");
const fileInput = document.querySelector("#reference-video");
const directVideoInput = document.querySelector("#direct-video-url");
const uploadSourcePanel = document.querySelector("#upload-source-panel");
const urlSourcePanel = document.querySelector("#url-source-panel");
const urlUploadRecovery = document.querySelector("#url-upload-recovery");
const signControl = document.querySelector("#sign-name");
const routineControl = document.querySelector("#routine-context");
const referenceModeInputs = [...document.querySelectorAll('input[name="reference_input_mode"]')];
const demoButton = document.querySelector("#use-demo-video");
const fileName = document.querySelector("#selected-file-name");
const fileMeta = document.querySelector("#selected-file-meta");
const runButton = document.querySelector("#run-movement-check");
const retryButton = document.querySelector("#reset-sign-run");
const formMessage = document.querySelector("#sign-form-message");
const serviceState = document.querySelector("#service-state");
const processingNote = document.querySelector("#processing-note");
const stageList = document.querySelector("#processing-stages");
const resultSection = document.querySelector("#result-section");
const reviewSection = document.querySelector("#review-section");
const illustrativeMotionSection = document.querySelector("#illustrative-motion-section");
const visualPreparationSection = document.querySelector("#visual-preparation-section");
const visualReviewSection = document.querySelector("#visual-review-section");
const downstreamSection = document.querySelector("#downstream-section");

const escapeQuery = (value) => encodeURIComponent(value || "");
const scrollToSection = (element, block = "start") => element.scrollIntoView({
  behavior: window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ? "auto" : "smooth",
  block
});

const PRODUCT_STAGE_LABELS = [
  "Sign & reference",
  "Review reference",
  "Choose poses",
  "Approve visual",
  "Family materials"
];

const setProductStage = (currentStep) => {
  const safeStep = Math.min(PRODUCT_STAGE_LABELS.length, Math.max(1, Number(currentStep) || 1));
  document.querySelectorAll("[data-product-step]").forEach((item) => {
    const step = Number(item.dataset.productStep);
    const marker = item.querySelector(".product-step-marker");
    item.classList.toggle("is-complete", step < safeStep);
    item.classList.toggle("is-current", step === safeStep);
    item.classList.toggle("is-upcoming", step > safeStep);
    if (step === safeStep) item.setAttribute("aria-current", "step");
    else item.removeAttribute("aria-current");
    if (marker) marker.textContent = step < safeStep ? "✓" : String(step).padStart(2, "0");
  });
  setText("#sign-progress-count", `Step ${safeStep} of ${PRODUCT_STAGE_LABELS.length}`);
  setText("#sign-progress-label", PRODUCT_STAGE_LABELS[safeStep - 1]);
  document.querySelector("#sign-progress-bar").style.width = `${safeStep / PRODUCT_STAGE_LABELS.length * 100}%`;
};

const renderStages = (stages = STAGES.map(([key, label]) => ({ key, label, status: "Waiting" }))) => {
  stageList.replaceChildren(...stages.map((stage, index) => {
    const item = document.createElement("li");
    item.dataset.status = stage.status.toLowerCase().replaceAll(" ", "-");
    const number = document.createElement("span");
    number.textContent = String(index + 1).padStart(2, "0");
    const label = document.createElement("strong");
    label.textContent = STAGE_LABELS[stage.key] || "Reference review";
    const status = document.createElement("small");
    status.textContent = stage.status;
    item.append(number, label, status);
    return item;
  }));
};

const sourceInstruction = (mode = state.inputMode) => mode === "url"
  ? "Enter a direct MP4 video URL."
  : "Select an MP4 from this computer.";

const syncReferenceInputMode = (mode, { clearSelection = true } = {}) => {
  if (state.submissionPending) return;
  state.inputMode = mode === "url" ? "url" : "upload";
  referenceModeInputs.forEach((input) => {
    input.checked = input.value === state.inputMode;
  });
  uploadSourcePanel.hidden = state.inputMode !== "upload";
  urlSourcePanel.hidden = state.inputMode !== "url";
  fileInput.disabled = state.inputMode !== "upload";
  directVideoInput.disabled = state.inputMode !== "url";
  urlUploadRecovery.hidden = true;
  if (clearSelection) {
    state.source = null;
    state.file = null;
    fileInput.value = "";
    directVideoInput.value = "";
    signControl.disabled = false;
    runButton.disabled = true;
    fileName.textContent = "No video selected";
    fileMeta.textContent = "MP4 · maximum 100 MB";
    document.querySelector("#direct-video-meta").textContent = "Maximum 100 MB · fetched by the local KinderFlow service";
    formMessage.textContent = sourceInstruction();
  } else {
    signControl.disabled = state.source === "demo";
    runButton.disabled = !state.source;
  }
};

const setSelectedSource = (source, selectedFile = null) => {
  if (state.submissionPending) return;
  state.source = source;
  state.file = selectedFile;
  state.inputMode = source === "url" ? "url" : "upload";
  referenceModeInputs.forEach((input) => {
    input.checked = input.value === state.inputMode;
  });
  uploadSourcePanel.hidden = state.inputMode !== "upload";
  urlSourcePanel.hidden = state.inputMode !== "url";
  fileInput.disabled = state.inputMode !== "upload";
  directVideoInput.disabled = state.inputMode !== "url";
  urlUploadRecovery.hidden = true;
  runButton.disabled = false;
  if (source === "demo") {
    fileInput.value = "";
    directVideoInput.value = "";
    signControl.value = "MORE";
    signControl.disabled = true;
    fileName.textContent = "Included MORE reference";
    fileMeta.textContent = "Demo reference · stored on this computer";
    formMessage.textContent = "MORE reference video selected. Ready for review.";
  } else if (source === "upload") {
    signControl.disabled = false;
    directVideoInput.value = "";
  } else {
    signControl.disabled = false;
    state.file = null;
    fileInput.value = "";
    document.querySelector("#direct-video-meta").textContent = "Direct MP4 selected · maximum 100 MB";
    formMessage.textContent = "Direct video URL selected. Ready for review.";
  }
};

const setReferenceControlsLocked = (locked) => {
  referenceModeInputs.forEach((input) => { input.disabled = locked; });
  routineControl.disabled = locked;
  demoButton.disabled = locked;
  urlUploadRecovery.disabled = locked;
  if (locked) {
    signControl.disabled = true;
    fileInput.disabled = true;
    directVideoInput.disabled = true;
    runButton.disabled = true;
    return;
  }
  signControl.disabled = state.source === "demo";
  fileInput.disabled = state.inputMode !== "upload";
  directVideoInput.disabled = state.inputMode !== "url";
  runButton.disabled = !state.source;
};

const resetRun = () => {
  if (state.polling) window.clearTimeout(state.polling);
  state.polling = null;
  state.submissionPending = false;
  state.runGeneration += 1;
  state.run = null;
  resultSection.hidden = true;
  reviewSection.hidden = true;
  illustrativeMotionSection.hidden = true;
  clearIllustrativeVideo();
  visualPreparationSection.hidden = true;
  visualReviewSection.hidden = true;
  downstreamSection.hidden = true;
  state.activePackage = null;
  state.selectedCandidate = null;
  state.currentCandidates = [];
  state.evidenceRoute = null;
  state.selectedFrames = [];
  state.workflowRecord = null;
  sessionStorage.removeItem("kinderflowReferenceReview");
  sessionStorage.removeItem("kinderflowVisualWorkflow");
  sessionStorage.removeItem("kinderflowApprovedVisual");
  sessionStorage.removeItem("kinderflowPrintableApproval");
  document.querySelector("#visual-candidates").replaceChildren();
  const generateButton = document.querySelector("#generate-visual-candidates");
  generateButton.disabled = false;
  generateButton.textContent = "Create visual options";
  const regenerateButton = document.querySelector("#regenerate-candidate");
  regenerateButton.disabled = false;
  const approveVisualButton = document.querySelector("#approve-visual");
  approveVisualButton.disabled = true;
  approveVisualButton.textContent = "Approve selected visual";
  retryButton.hidden = true;
  const approve = document.querySelector("#approve-sign");
  approve.hidden = false;
  approve.disabled = false;
  approve.textContent = "Create family materials";
  document.querySelector("#use-another-reference").hidden = false;
  document.querySelector("#use-another-reference").textContent = "Use another reference";
  document.querySelector("#tracked-pose-availability").hidden = true;
  const reviewState = document.querySelector("#review-state");
  reviewState.textContent = "Review recommended";
  reviewState.className = "status-pill status-review";
  setText("#review-message", "Choose how to continue.");
  setText("#frame-picker-help", "Select at least one pose to continue.");
  document.querySelector("#technical-review-rationale").value = "";
  document.querySelector("#technical-review-rationale").disabled = false;
  document.querySelector("#suggested-reference-frames").replaceChildren();
  form.querySelectorAll("input, select, button").forEach((control) => { control.disabled = false; });
  syncReferenceInputMode(state.inputMode, { clearSelection: false });
  renderStages();
  processingNote.textContent = state.source ? "Reference selected. Ready to run." : "Waiting for a reference video.";
  formMessage.textContent = state.source ? "Ready to review the reference." : "Select an MP4 or use the demo reference.";
  setProductStage(1);
};

const clearReference = () => {
  resetRun();
  state.source = null;
  state.file = null;
  fileInput.value = "";
  directVideoInput.value = "";
  fileName.textContent = "No video selected";
  fileMeta.textContent = "MP4 · maximum 100 MB";
  signControl.disabled = false;
  runButton.disabled = true;
  syncReferenceInputMode(state.inputMode, { clearSelection: true });
  scrollToSection(document.querySelector(".create-sign-setup"));
};

const formatBytes = (bytes) => bytes < 1024 * 1024
  ? `${Math.max(1, Math.round(bytes / 1024))} KB`
  : `${(bytes / 1024 / 1024).toFixed(1)} MB`;

fileInput.addEventListener("change", () => {
  if (state.submissionPending) return;
  const selected = fileInput.files[0];
  if (!selected) return;
  if (!selected.name.toLowerCase().endsWith(".mp4")) {
    state.source = null;
    state.file = null;
    runButton.disabled = true;
    fileName.textContent = "Unsupported file";
    fileMeta.textContent = "MP4 is required";
    formMessage.textContent = "Please select a supported MP4 video.";
    return;
  }
  fileName.textContent = selected.name;
  fileMeta.textContent = `${formatBytes(selected.size)} · selected from this computer`;
  setSelectedSource("upload", selected);
  formMessage.textContent = "Reference video selected. Ready for review.";
});

directVideoInput.addEventListener("input", () => {
  if (state.submissionPending) return;
  const value = directVideoInput.value.trim();
  state.file = null;
  state.source = value ? "url" : null;
  signControl.disabled = false;
  runButton.disabled = !value;
  urlUploadRecovery.hidden = true;
  document.querySelector("#direct-video-meta").textContent = value
    ? "Direct MP4 selected · maximum 100 MB"
    : "Maximum 100 MB · fetched by the local KinderFlow service";
  formMessage.textContent = value
    ? "Direct video URL selected. Ready for review."
    : "Enter a direct MP4 video URL.";
});

referenceModeInputs.forEach((input) => {
  input.addEventListener("change", () => syncReferenceInputMode(input.value));
});

demoButton.addEventListener("click", () => setSelectedSource("demo"));
urlUploadRecovery.addEventListener("click", () => {
  syncReferenceInputMode("upload");
  fileInput.focus();
});
retryButton.addEventListener("click", clearReference);

const requestRun = async (selection) => {
  const { source, signName, routineContext, directVideoUrl, file } = selection;
  const referenceStatus = INTERNAL_REFERENCE_STATUS;
  if (!signName || !routineContext) throw new Error("Complete the sign name and routine before processing.");
  if (!source) throw new Error(sourceInstruction());

  if (source === "demo") {
    return fetch("/api/runs/demo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sign_name: signName, routine_context: routineContext, reference_status: referenceStatus })
    });
  }
  if (source === "url") {
    let parsed;
    try {
      parsed = new URL(directVideoUrl);
    } catch (_error) {
      throw new Error("Enter a complete http:// or https:// direct video URL.");
    }
    if (!["http:", "https:"].includes(parsed.protocol)) {
      throw new Error("Enter a complete http:// or https:// direct video URL.");
    }
    return fetch("/api/runs/url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sign_name: signName, routine_context: routineContext, reference_status: referenceStatus, direct_video_url: directVideoUrl })
    });
  }
  const payload = new FormData();
  payload.append("sign_name", signName);
  payload.append("routine_context", routineContext);
  payload.append("reference_status", referenceStatus);
  payload.append("reference_video", file);
  return fetch("/api/runs/upload", { method: "POST", body: payload });
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (state.submissionPending) return;
  const selection = {
    source: state.source,
    signName: signControl.value.trim(),
    routineContext: routineControl.value.trim(),
    directVideoUrl: directVideoInput.value.trim(),
    file: state.file
  };
  const generation = state.runGeneration + 1;
  state.runGeneration = generation;
  state.submissionPending = true;
  setReferenceControlsLocked(true);
  sessionStorage.removeItem("kinderflowApprovedVisual");
  sessionStorage.removeItem("kinderflowPrintableApproval");
  retryButton.hidden = true;
  resultSection.hidden = true;
  reviewSection.hidden = true;
  illustrativeMotionSection.hidden = true;
  clearIllustrativeVideo();
  visualPreparationSection.hidden = true;
  visualReviewSection.hidden = true;
  downstreamSection.hidden = true;
  formMessage.textContent = "Preparing the reference review…";
  processingNote.textContent = "Starting the reference review. Processing may take about a minute.";
  renderStages(STAGES.map(([key, label], index) => ({ key, label, status: index === 0 ? "Running" : "Waiting" })));
  setProductStage(2);
  scrollToSection(document.querySelector("#processing-section"));
  try {
    const response = await requestRun(selection);
    if (generation !== state.runGeneration) return;
    const payload = await response.json();
    if (generation !== state.runGeneration) return;
    if (!response.ok) throw new Error(payload.error || "The reference review could not be started.");
    state.run = payload;
    if (selection.source === "url") {
      directVideoInput.value = payload.source?.reference_source_url || "";
    }
    state.submissionPending = false;
    setReferenceControlsLocked(true);
    retryButton.disabled = false;
    formMessage.textContent = "Reference review started.";
    pollRun(payload.run_id, generation);
  } catch (error) {
    if (generation !== state.runGeneration) return;
    state.submissionPending = false;
    setReferenceControlsLocked(false);
    syncReferenceInputMode(state.inputMode, { clearSelection: false });
    formMessage.textContent = error.message;
    processingNote.textContent = "The reference review could not be started.";
    urlUploadRecovery.hidden = selection.source !== "url";
    retryButton.hidden = false;
    retryButton.disabled = false;
  }
});

const pollRun = async (runId, generation = state.runGeneration) => {
  try {
    const response = await fetch(`/api/runs/${encodeURIComponent(runId)}`, { cache: "no-store" });
    if (generation !== state.runGeneration) return;
    if (!response.ok) throw new Error("Run status is unavailable.");
    const run = await response.json();
    if (generation !== state.runGeneration) return;
    state.run = run;
    renderStages(run.stages);
    const active = run.stages.find((stage) => stage.status === "Running");
    processingNote.textContent = active ? `${STAGE_LABELS[active.key] || "Reference review"} is running on this computer…` : `${RUN_STATE_COPY[run.state] || "Reference review updated"}.`;
    if (["complete", "failed", "insufficient_coverage"].includes(run.state)) {
      finishRun(run);
      return;
    }
    state.polling = window.setTimeout(() => pollRun(runId, generation), 900);
  } catch (error) {
    if (generation !== state.runGeneration) return;
    processingNote.textContent = `${error.message} Select another reference video.`;
    retryButton.hidden = false;
    retryButton.disabled = false;
  }
};

const setText = (selector, value) => { document.querySelector(selector).textContent = value; };

const normalizeSignId = (value) => (value || "")
  .trim()
  .toLowerCase()
  .replaceAll(/[^a-z0-9]+/g, "_")
  .replaceAll(/^_+|_+$/g, "");

const friendlyReviewReason = (reason) => {
  const copy = String(reason || "");
  const handCoverage = copy.match(/Dominant-hand landmarks were detected in ([0-9.]+)% of frames\./i);
  if (handCoverage) return `The main hand was visible in ${handCoverage[1]}% of the video.`;
  const unresolved = copy.match(/(\d+) unresolved frames \(([0-9.]+)%\) remain\./i);
  if (unresolved) return `${unresolved[1]} frames (${unresolved[2]}%) need review.`;
  if (/grounded fallback/i.test(copy)) return "Some of the hand movement near the face was not visible throughout the video. You can continue using the reviewed sign references or choose another video.";
  if (/Long or edge movement gaps/i.test(copy)) return "Some movement at the beginning or end of the video needs review.";
  if (/body reference was not available/i.test(copy)) return "The body position was not visible consistently.";
  if (/Abrupt movement transitions/i.test(copy)) return "Some movement changes need review.";
  if (/Technical capture is sufficient/i.test(copy)) return "The reference movement is clear enough to continue.";
  if (/Technical issues should be reviewed/i.test(copy)) return "This reference needs review before continuing.";
  return copy
    .replaceAll(/dominant-hand landmarks/gi, "main-hand visibility")
    .replaceAll(/unresolved frames/gi, "frames needing review")
    .replaceAll(/grounded fallback/gi, "reviewed references");
};

const friendlyRunError = (error) => {
  const message = String(error?.message || "");
  if (/preview|ffmpeg|encoding/i.test(message)) return "The pose preview could not be prepared. Try another reference or ask an administrator to check the local service.";
  if (/movement data|hands visible|coverage/i.test(message)) return "Not enough of the sign was visible for review. Try a clearer reference video with the hands in view.";
  return message && !/[A-Z_]{3,}/.test(message) ? message : "The reference review could not be completed. Choose another reference video and try again.";
};

const trackedPosesAreAvailable = (run) => {
  const coverage = Number(run?.metrics?.dominant_hand_detection_coverage_percent);
  return Number.isFinite(coverage) && coverage >= TRACKED_POSE_MINIMUM_PERCENT;
};

const evidenceRouteIsAvailable = (route, run) => {
  if (route === "LANDMARK_KEY_POSE") return trackedPosesAreAvailable(run);
  if (route === "HUMAN_SELECTED_FRAME") return Boolean(run?.artifacts?.suggested_reference_frames?.length);
  return route === "KNOWLEDGE_REFERENCE_FALLBACK";
};

const availableRouteForRun = (run, signPackage, requestedRoute = null) => {
  if (requestedRoute && evidenceRouteIsAvailable(requestedRoute, run)) return requestedRoute;
  const configuredRoute = routeForRun(run, signPackage);
  if (evidenceRouteIsAvailable(configuredRoute, run)) return configuredRoute;
  if (trackedPosesAreAvailable(run)) return "LANDMARK_KEY_POSE";
  if (run?.artifacts?.suggested_reference_frames?.length) return "HUMAN_SELECTED_FRAME";
  return "KNOWLEDGE_REFERENCE_FALLBACK";
};

const visualPackageIsReady = (signPackage) => {
  if (!signPackage || !Array.isArray(signPackage.candidates) || signPackage.candidates.length === 0) return false;
  const declaredStates = [signPackage.status, signPackage.readiness_status, signPackage.visual_status, signPackage.review_status]
    .filter(Boolean)
    .map((value) => String(value).toUpperCase());
  return !declaredStates.some((value) => value === "NOT_READY" || value === "UNSUPPORTED");
};

const loadVisualPackages = async () => {
  const response = await fetch("data/visual_sign_packages.json", { cache: "no-store" });
  if (!response.ok) throw new Error("Sign visuals are unavailable.");
  const payload = await response.json();
  if (!Array.isArray(payload.signs)) throw new Error("Sign visuals could not be read.");
  state.visualPackages = payload.signs;
};

const loadIllustrativeVideoCatalog = async () => {
  const response = await fetch("/api/illustrative-videos", { cache: "no-store" });
  if (!response.ok) throw new Error("Illustrative video information is unavailable.");
  const payload = await response.json();
  if (!payload.signs || typeof payload.signs !== "object") {
    throw new Error("Illustrative video information could not be read.");
  }
  state.illustrativeCatalog = payload.signs;
};

const clearIllustrativeVideo = () => {
  const video = document.querySelector("#illustrative-video");
  video.onloadedmetadata = null;
  video.onerror = null;
  video.pause();
  video.removeAttribute("src");
  video.load();
};

const showIllustrativeVideoMissing = () => {
  clearIllustrativeVideo();
  document.querySelector("#illustrative-video-available").hidden = true;
  document.querySelector("#illustrative-video-missing").hidden = false;
  document.querySelector("#illustrative-primary-disclosure").hidden = true;
  document.querySelector("#illustrative-technical-details").hidden = true;
};

const renderIllustrativeVideo = () => {
  const signId = state.activePackage?.sign_id || normalizeSignId(state.run?.sign?.sign_id || state.run?.sign?.name);
  const entry = state.illustrativeCatalog[signId];
  illustrativeMotionSection.hidden = false;
  clearIllustrativeVideo();
  document.querySelector("#illustrative-video-missing").hidden = true;
  document.querySelector("#illustrative-primary-disclosure").hidden = false;
  document.querySelector("#illustrative-technical-details").hidden = false;
  if (!entry || entry.available !== true || !entry.url) {
    showIllustrativeVideoMissing();
    return;
  }

  const video = document.querySelector("#illustrative-video");
  const available = document.querySelector("#illustrative-video-available");
  const status = document.querySelector("#illustrative-video-status");
  available.hidden = false;
  video.setAttribute("aria-label", `${entry.label || signId.toUpperCase()} illustrative video preview`);
  setText("#illustrative-provider", entry.provider || "Google Labs FX / Gemini FX");
  setText(
    "#illustrative-usage",
    entry.usage_status === "GOOGLE_LABS_FX_OUTPUT_USAGE_CONFIRMATION_NEEDED"
      ? "Local demo; external usage confirmation needed"
      : "Usage status unavailable; do not display externally"
  );
  status.textContent = "Loading illustrative video…";
  video.onloadedmetadata = () => {
    status.textContent = Number.isFinite(video.duration) && video.duration > 0
      ? `Ready · ${video.duration.toFixed(1)} seconds`
      : "The illustrative preview metadata is incomplete.";
  };
  video.onerror = () => {
    showIllustrativeVideoMissing();
  };
  video.src = entry.url;
  video.load();
};

const ROUTE_COPY = {
  LANDMARK_KEY_POSE: {
    level: 1, title: "Tracked poses", note: "Reviewed sign guidance, clear tracked poses and the trusted sign reference.", status: "Ready"
  },
  HUMAN_SELECTED_FRAME: {
    level: 2, title: "Selected reference frames", note: "Reviewed sign guidance and the reference poses selected for this visual.", status: "Selected"
  },
  KNOWLEDGE_REFERENCE_FALLBACK: {
    level: 3, title: "Reviewed references", note: "Reviewed sign guidance, the trusted sign reference and any clear movement information.", status: "Review required"
  },
  INTERNAL_POSE_GUIDE: {
    level: 4, title: "Reviewed pose guide", note: "A controlled pose guide for visual review, not final artwork.", status: "Review required"
  }
};

const routeForRun = (run, signPackage) => {
  if (!signPackage?.evidence_routes) return null;
  if (run.technical_status === "Pass") return signPackage.evidence_routes.pass;
  if (run.technical_status === "Review needed") return signPackage.evidence_routes.review;
  return signPackage.evidence_routes.fallback;
};

const routeCopy = () => ROUTE_COPY[state.evidenceRoute] || ROUTE_COPY.KNOWLEDGE_REFERENCE_FALLBACK;

const persistWorkflowRecord = (updates = {}) => {
  const now = new Date().toISOString();
  const base = state.workflowRecord || {
    sign_id: state.activePackage?.sign_id || normalizeSignId(state.run?.sign?.sign_id || state.run?.sign?.name),
    cv_run_id: state.run?.run_id || null,
    routine_context: state.run?.sign?.routine_context || "",
    technical_status: (state.run?.technical_status || "Waiting").toUpperCase().replaceAll(" ", "_"),
    technical_review_action: null,
    technical_review_rationale: "",
    visual_evidence_route: state.evidenceRoute,
    candidate_ids: [],
    selected_candidate_id: null,
    visual_review_status: "NOT_STARTED",
    internal_printable_eligible: false,
    publication_status: "DRAFT",
    last_updated: now
  };
  state.workflowRecord = { ...base, ...updates, publication_status: "DRAFT", last_updated: now };
  sessionStorage.setItem("kinderflowVisualWorkflow", JSON.stringify(state.workflowRecord));
};

const readStoredPayload = (key) => {
  try {
    return JSON.parse(sessionStorage.getItem(key) || "null");
  } catch (_error) {
    return null;
  }
};

const allPackageCandidates = () => state.activePackage
  ? [...state.activePackage.candidates, ...(state.activePackage.regeneration_candidates || [])]
  : [];

const updateFamilyMaterialLinks = () => {
  if (!state.run || !state.activePackage || !state.selectedCandidate) return;
  const sign = state.run.sign;
  const printableApproval = readStoredPayload("kinderflowPrintableApproval");
  const printablePreferences = readStoredPayload("kinderflowPrintablePreferences");
  const preferredLanguage = (
    printableApproval?.sign_id === state.activePackage.sign_id
    && ["en", "es"].includes(printableApproval.language)
  ) ? printableApproval.language : (
    printablePreferences?.sign_id === state.activePackage.sign_id
    && ["en", "es"].includes(printablePreferences.language)
  ) ? printablePreferences.language : "en";
  const common = {
    sign: sign.name,
    routine: sign.routine_context,
    source_run: state.run.run_id,
    visual: state.selectedCandidate.id,
    approved: "1"
  };
  document.querySelector("#create-printable-link").href = `flashcards.html?${new URLSearchParams({ ...common, restore: "1", type: "flashcard", lang: preferredLanguage }).toString()}`;
  document.querySelector("#create-routine-link").href = `flashcards.html?${new URLSearchParams({ ...common, restore: "1", type: "routine", lang: preferredLanguage }).toString()}`;
  const storyLink = document.querySelector("#create-story-link");
  const storyAvailabilityNote = document.querySelector("#story-availability-note");
  const storyIsAvailable = normalizeSignId(sign.name) === "more";
  storyLink.hidden = !storyIsAvailable;
  storyAvailabilityNote.hidden = storyIsAvailable;
  if (storyIsAvailable) storyLink.href = `create-story.html?${new URLSearchParams(common).toString()}`;
};

const markReferenceReviewComplete = () => {
  const reviewState = document.querySelector("#review-state");
  reviewState.textContent = "Reference review complete";
  reviewState.className = "status-pill status-ready";
  setText("#content-status", "Ready to create visual options");
  setText("#review-title", "Reference poses ready");
  setText("#review-guidance", "The reference review is saved. Continue to create the visual options.");
  setText("#review-message", "Your reference choice is saved.");
  document.querySelectorAll('input[name="evidence_route"]').forEach((input) => { input.disabled = true; });
  document.querySelector("#suggested-reference-frames").querySelectorAll('input[type="checkbox"]').forEach((input) => { input.disabled = true; });
  document.querySelector("#technical-review-rationale").disabled = true;
};

const updatePoseSelectionUi = () => {
  const isFrames = state.evidenceRoute === "HUMAN_SELECTED_FRAME";
  const container = document.querySelector("#suggested-reference-frames");
  const inputs = [...container.querySelectorAll('input[type="checkbox"]')];
  state.selectedFrames = inputs.filter((input) => input.checked).map((input) => input.value);
  const count = state.selectedFrames.length;
  inputs.forEach((input) => {
    input.disabled = isFrames && count >= 2 && !input.checked;
  });
  document.querySelector("#approve-sign").disabled = isFrames && (count < 1 || count > 2);
  if (isFrames) {
    setText(
      "#frame-picker-help",
      count === 0 ? "Select at least one pose to continue." : `${count} pose${count === 1 ? "" : "s"} selected`
    );
    setText("#source-detail-frames", count === 0 ? "Not selected" : `${count} selected`);
  } else {
    setText("#source-detail-frames", "Not needed for this pose source");
  }
};

const updateEvidenceRouteUi = () => {
  const route = state.evidenceRoute;
  const isFrames = route === "HUMAN_SELECTED_FRAME";
  const isFallback = route === "KNOWLEDGE_REFERENCE_FALLBACK";
  document.querySelector("#reference-frame-picker").hidden = !isFrames;
  document.querySelector("#fallback-rationale-field").hidden = !isFallback;
  setText("#source-detail-route", ROUTE_COPY[route]?.title || "Not selected");
  const action = document.querySelector("#approve-sign");
  action.textContent = "Create family materials";
  setText("#review-message", isFallback
    ? "Continue with reviewed references after adding a short reason."
    : isFrames ? "Select the clearest reference poses." : "The tracked poses are ready to use.");
  updatePoseSelectionUi();
};

const renderSuggestedFrames = (frames = []) => {
  state.selectedFrames = [];
  const container = document.querySelector("#suggested-reference-frames");
  if (!frames.length) {
    container.replaceChildren();
    setText("#frame-picker-help", "Suggested frames are unavailable. Use reviewed references or choose another video.");
    return;
  }
  container.replaceChildren(...frames.slice(0, 6).map((frame) => {
    const label = document.createElement("label");
    const input = document.createElement("input");
    input.type = "checkbox";
    input.value = frame.id;
    input.setAttribute("aria-label", frame.label);
    input.addEventListener("change", () => {
      if (state.workflowRecord?.technical_review_action) {
        input.checked = state.selectedFrames.includes(input.value);
        return;
      }
      if (input.checked && container.querySelectorAll("input:checked").length > 2) input.checked = false;
      updatePoseSelectionUi();
      persistWorkflowRecord({ selected_reference_frames: [...state.selectedFrames] });
    });
    const image = document.createElement("img");
    image.src = frame.url;
    image.alt = `${frame.label}, suggested still from the reference video`;
    const text = document.createElement("span");
    text.textContent = frame.label;
    label.append(input, image, text);
    return label;
  }));
  updatePoseSelectionUi();
};

const loadRunVideo = (video, status, url, runId) => {
  video.pause();
  video.removeAttribute("src");
  video.load();
  status.textContent = "Loading video metadata…";
  const finalUrl = `${url}${url.includes("?") ? "&" : "?"}run=${encodeURIComponent(runId)}`;
  video.onloadedmetadata = () => {
    if (Number.isFinite(video.duration) && video.duration > 0) {
      video.currentTime = 0;
      status.textContent = `Ready · ${video.duration.toFixed(1)} seconds`;
    } else {
      status.textContent = "Video metadata is incomplete. Use another reference video.";
    }
  };
  video.onerror = () => {
    status.textContent = "This video preview could not be loaded. Use another reference video.";
  };
  video.src = finalUrl;
  video.load();
};

const finishRun = (run, { scroll = true } = {}) => {
  retryButton.hidden = false;
  retryButton.disabled = false;
  formMessage.textContent = run.state === "complete" ? "Reference review complete." : friendlyRunError(run.error) || "Reference review finished with limited information.";
  const isComplete = run.state === "complete";
  const selectedSignId = normalizeSignId(run.sign?.sign_id || run.sign?.name);
  state.activePackage = state.visualPackages.find((item) => normalizeSignId(item.sign_id) === selectedSignId) || null;
  state.evidenceRoute = availableRouteForRun(run, state.activePackage);
  const reviewIsUsable = isComplete && ["Pass", "Review needed"].includes(run.technical_status);
  const canPrepare = reviewIsUsable && visualPackageIsReady(state.activePackage);
  formMessage.textContent = reviewIsUsable
    ? "Reference review complete."
    : "This reference video cannot be used. Choose another reference to continue.";
  state.currentCandidates = canPrepare ? [...state.activePackage.candidates] : [];
  const isSupportedSign = SUPPORTED_SIGN_IDS.has(selectedSignId);
  const hasMetrics = Boolean(run.metrics);
  const hasArtifacts = Boolean(run.artifacts && run.artifacts.reference_video_url);
  const statusCopy = TECHNICAL_STATUS_COPY[run.technical_status] || { label: "Reference review unavailable", explanation: friendlyRunError(run.error) };
  setText("#result-kicker", "Reference review");
  setText("#result-title", reviewIsUsable ? "Reference review complete" : "Choose another reference video");
  setText(
    "#result-explanation",
    reviewIsUsable
      ? "We found a few moments worth checking before creating the family materials."
      : "This reference video cannot be used. Choose another reference to continue."
  );
  processingNote.textContent = isComplete
    ? "Results ready. Review the summary and visual evidence below."
    : friendlyRunError(run.error);
  setText("#technical-status", reviewIsUsable ? "Complete" : statusCopy.label);
  setText("#raw-technical-status", run.technical_status);
  setText(
    "#content-status",
    canPrepare
      ? "Choose the clearest poses"
      : !reviewIsUsable ? "Choose another reference" : isSupportedSign ? "Illustration not prepared" : "Sign not available"
  );
  setText("#run-identifier", "Reference ready");
  setText("#source-detail-run", run.run_id);
  const sourceUrl = run.source?.reference_source_url;
  const sourceDetail = document.querySelector("#source-detail-url");
  sourceDetail.replaceChildren();
  if (sourceUrl) {
    const link = document.createElement("a");
    link.href = sourceUrl;
    link.target = "_blank";
    link.rel = "noopener";
    link.textContent = "View source";
    sourceDetail.append(link);
  } else {
    sourceDetail.textContent = run.source?.kind === "demo_reference"
      ? "Included MORE reference"
      : run.source?.kind === "operator_upload"
        ? "Uploaded video"
        : "Not provided";
  }
  document.querySelector("#movement-comparison").hidden = !hasArtifacts;
  document.querySelector("#technical-details").hidden = !hasMetrics;
  const movementPreview = document.querySelector("#movement-video-preview");
  const movementPlaybackStatus = document.querySelector("#movement-playback-status");
  const hasMovementPreview = Boolean(run.artifacts?.movement_preview_url);
  document.querySelector("#movement-preview-panel").hidden = !hasMovementPreview;
  if (!hasMovementPreview) {
    movementPreview.pause?.();
    movementPreview.removeAttribute("src");
    movementPlaybackStatus.textContent = "Pose preview is unavailable for this reference.";
  }
  const timelineLink = document.querySelector("#detection-timeline-link");
  const wristLink = document.querySelector("#wrist-trajectory-link");
  timelineLink.hidden = !run.artifacts?.detection_timeline_url;
  wristLink.hidden = !run.artifacts?.wrist_trajectory_url;
  if (timelineLink.hidden) document.querySelector("#detection-timeline").removeAttribute("src");
  if (wristLink.hidden) document.querySelector("#wrist-trajectory").removeAttribute("src");
  if (hasMetrics) {
    setText("#metric-frames", run.metrics.frames_analysed);
    setText("#metric-pose", `${run.metrics.pose_detection_coverage_percent}%`);
    setText("#metric-hand", `${run.metrics.dominant_hand_detection_coverage_percent}%`);
    setText("#metric-missing", run.metrics.missing_hand_frames);
    setText("#metric-unresolved", `${run.metrics.unresolved_frames} (${run.metrics.unresolved_frames_percent}%)`);
  }
  setText("#metric-duration", `${run.processing.duration_seconds}s`);
  if (hasArtifacts) {
    loadRunVideo(
      document.querySelector("#reference-video-preview"),
      document.querySelector("#reference-playback-status"),
      run.artifacts.reference_video_url,
      run.run_id
    );
    if (run.artifacts.movement_preview_url) {
      loadRunVideo(
        movementPreview,
        movementPlaybackStatus,
        run.artifacts.movement_preview_url,
        run.run_id
      );
    }
    if (run.artifacts.detection_timeline_url) {
      const timeline = document.querySelector("#detection-timeline");
      timeline.src = run.artifacts.detection_timeline_url;
      timelineLink.href = run.artifacts.detection_timeline_url;
    }
    if (run.artifacts.wrist_trajectory_url) {
      const wrist = document.querySelector("#wrist-trajectory");
      wrist.src = run.artifacts.wrist_trajectory_url;
      wristLink.href = run.artifacts.wrist_trajectory_url;
    }
  }
  renderSuggestedFrames(run.artifacts?.suggested_reference_frames || []);
  const warnings = run.warnings?.length ? run.warnings : ["No additional technical warnings were recorded."];
  const warningList = document.querySelector("#technical-warnings");
  warningList.replaceChildren(...warnings.map((warning) => { const item = document.createElement("li"); item.textContent = warning; return item; }));
  const raw = run.technical_details || {};
  setText(
    "#raw-technical-statuses",
    raw.extraction_status
      ? `Raw processing states: ${raw.extraction_status} · ${raw.motion_representation_status} · ${raw.poc_feasibility_decision}`
      : ""
  );
  const reviewReasons = document.querySelector("#review-reasons");
  reviewReasons.replaceChildren();
  reviewReasons.hidden = true;
  const approveButton = document.querySelector("#approve-sign");
  approveButton.hidden = !canPrepare;
  approveButton.textContent = "Create family materials";
  if (canPrepare) {
    setText("#review-title", "Choose one or two reference poses");
    setText("#review-guidance", "Select the clearest moments to guide the visual.");
  } else if (!reviewIsUsable) {
    setText("#review-title", "Choose another reference video");
    setText("#review-guidance", "This reference video cannot be used. Choose another reference to continue.");
  } else if (isSupportedSign) {
    setText("#review-title", "Sign visual not ready");
    setText("#review-guidance", "This sign does not have a reviewed illustration yet. Choose another sign to continue.");
  } else {
    setText("#review-title", "Sign not available");
    setText("#review-guidance", "This sign is not available in the current demo set. Choose another sign to continue.");
  }
  const reviewState = document.querySelector("#review-state");
  reviewState.textContent = canPrepare
    ? "Review recommended"
    : !reviewIsUsable ? "Reference not usable" : isSupportedSign ? "Illustration not prepared" : "Sign not available";
  reviewState.className = "status-pill status-review";
  resultSection.hidden = false;
  reviewSection.hidden = false;
  const trackedPosesAvailable = canPrepare && trackedPosesAreAvailable(run);
  document.querySelectorAll('input[name="evidence_route"]').forEach((input) => {
    input.checked = input.value === state.evidenceRoute;
    input.disabled = (
      (input.value === "LANDMARK_KEY_POSE" && !trackedPosesAvailable)
      || (input.value === "HUMAN_SELECTED_FRAME" && !(run.artifacts?.suggested_reference_frames || []).length)
    );
  });
  document.querySelector("#tracked-pose-availability").hidden = trackedPosesAvailable;
  document.querySelector("#evidence-route-options").hidden = !canPrepare;
  document.querySelector("#reference-frame-picker").hidden = true;
  document.querySelector("#fallback-rationale-field").hidden = true;
  const recoveryButton = document.querySelector("#use-another-reference");
  recoveryButton.textContent = (canPrepare || !reviewIsUsable) ? "Use another reference" : "Choose another sign";
  persistWorkflowRecord();
  if (canPrepare) updateEvidenceRouteUi();
  else setText(
    "#review-message",
    !reviewIsUsable ? "Choose another reference video to continue." : "Choose another sign and add its reference video."
  );
  sessionStorage.setItem("kinderflowReferenceReview", JSON.stringify(run));
  setProductStage(canPrepare ? 3 : 2);
  if (scroll) scrollToSection(resultSection);
};

const renderVisualPreparation = () => {
  const signPackage = state.activePackage;
  document.querySelectorAll("[data-active-sign]").forEach((element) => { element.textContent = signPackage.labels.en; });
  document.querySelectorAll("[data-active-sign-es]").forEach((element) => { element.textContent = signPackage.labels.es; });
  document.querySelectorAll("[data-active-routine]").forEach((element) => { element.textContent = state.run.sign.routine_context; });
  setText("#grounding-source", "Reviewed sign guidance");
  setText("#grounding-source-note", "The reviewed sign information is ready.");
  setText("#grounding-source-status", "Ready");
  document.querySelector("#grounding-source-status").className = "grounding-status status-ready";
  setText("#grounding-motion", "Reference poses");
  setText("#grounding-motion-note", "The clearest movement moments are ready.");
  setText(
    "#grounding-motion-status",
    state.evidenceRoute === "HUMAN_SELECTED_FRAME" ? `${state.selectedFrames.length} selected` : "Ready"
  );
  document.querySelector("#grounding-motion-status").className = "grounding-status status-ready";
  setText("#grounding-character", "KinderFlow illustration");
  setText("#grounding-character-note", "The consistent family-facing style is ready.");
  setText("#grounding-character-status", "Ready");
  setText("#visual-brief-title", `${signPackage.movement.hands} ${signPackage.movement.hands === 1 ? "hand" : "hands"} · ${signPackage.movement.body_location.toLowerCase()} · ${signPackage.knowledge.direction.toLowerCase()} movement`);
  setText("#visual-brief-description", `${signPackage.movement.description} ${signPackage.movement.presentation}`);
  setText("#fallback-title", "Routine / context");
  setText("#visual-routine-context", state.run.sign.routine_context);
  setText("#visual-preparation-status", "Ready to create visual options for review.");
};

document.querySelectorAll('input[name="evidence_route"]').forEach((input) => {
  input.addEventListener("change", () => {
    if (state.workflowRecord?.technical_review_action) {
      input.checked = input.value === state.evidenceRoute;
      return;
    }
    state.evidenceRoute = input.value;
    if (state.evidenceRoute !== "HUMAN_SELECTED_FRAME") {
      document.querySelector("#suggested-reference-frames").querySelectorAll('input[type="checkbox"]').forEach((frame) => {
        frame.checked = false;
        frame.disabled = false;
      });
      state.selectedFrames = [];
    }
    if (state.evidenceRoute !== "KNOWLEDGE_REFERENCE_FALLBACK") {
      document.querySelector("#technical-review-rationale").value = "";
    }
    updateEvidenceRouteUi();
    persistWorkflowRecord({
      visual_evidence_route: state.evidenceRoute,
      selected_reference_frames: [...state.selectedFrames]
    });
  });
});

document.querySelector("#approve-sign").addEventListener("click", (event) => {
  if (!state.activePackage) return;
  if (state.evidenceRoute === "HUMAN_SELECTED_FRAME" && (state.selectedFrames.length < 1 || state.selectedFrames.length > 2)) {
    const selectionMessage = state.selectedFrames.length < 1
      ? "Select at least one pose to continue."
      : "Choose no more than two poses to continue.";
    setText("#frame-picker-help", selectionMessage);
    setText("#review-message", selectionMessage);
    scrollToSection(document.querySelector("#reference-frame-picker"), "center");
    return;
  }
  const rationale = state.evidenceRoute === "KNOWLEDGE_REFERENCE_FALLBACK"
    ? document.querySelector("#technical-review-rationale").value.trim()
    : "";
  if (state.evidenceRoute === "KNOWLEDGE_REFERENCE_FALLBACK" && !rationale) {
    setText("#review-message", "Add a short reason for using reviewed references.");
    document.querySelector("#technical-review-rationale").focus();
    return;
  }
  const action = state.evidenceRoute === "KNOWLEDGE_REFERENCE_FALLBACK" ? "ACCEPT_WITH_FALLBACK" : "ACCEPT_FOR_VISUAL_PREPARATION";
  persistWorkflowRecord({
    technical_review_action: action,
    technical_review_rationale: rationale || `Reviewer selected ${routeCopy().title.toLowerCase()} after reviewing the reference.`,
    visual_evidence_route: state.evidenceRoute,
    selected_reference_frames: state.evidenceRoute === "HUMAN_SELECTED_FRAME" ? [...state.selectedFrames] : [],
    visual_review_status: "READY_TO_GENERATE",
    internal_printable_eligible: false
  });
  event.currentTarget.disabled = true;
  event.currentTarget.textContent = "Pose choice saved";
  document.querySelector("#use-another-reference").hidden = true;
  markReferenceReviewComplete();
  renderVisualPreparation();
  illustrativeMotionSection.hidden = true;
  visualPreparationSection.hidden = false;
  setProductStage(4);
  scrollToSection(visualPreparationSection);
});

const createCandidateCard = (candidate, index) => {
  const label = document.createElement("label");
  label.className = "visual-candidate-card";
  const input = document.createElement("input");
  input.type = "radio";
  input.name = "visual_candidate";
  input.value = candidate.id;
  input.addEventListener("change", () => {
    state.selectedCandidate = candidate;
    document.querySelectorAll(".visual-candidate-card").forEach((card) => card.classList.remove("is-selected"));
    label.classList.add("is-selected");
    document.querySelector("#approve-visual").disabled = false;
    setText("#visual-review-status", `Option ${String.fromCharCode(65 + index)} selected. Check the hands and movement cue, then approve the visual.`);
  });
  const imageFrame = document.createElement("div");
  imageFrame.className = "candidate-image-frame";
  const image = document.createElement("img");
  image.src = candidate.asset;
  image.alt = `${candidate.title} for the ${state.activePackage.labels.en} sign`;
  imageFrame.append(image);
  const body = document.createElement("div");
  body.className = "candidate-card-body";
  const top = document.createElement("div");
  const badge = document.createElement("span");
  badge.className = "candidate-label";
  badge.textContent = `Option ${String.fromCharCode(65 + index)}`;
  const recommendation = document.createElement("span");
  recommendation.className = "candidate-recommendation";
  recommendation.textContent = "Recommended for this sign";
  top.append(badge);
  if (candidate.recommended === true) top.append(recommendation);
  const title = document.createElement("h3");
  title.textContent = candidate.title;
  const note = document.createElement("p");
  note.textContent = candidate.review_note;
  const checks = document.createElement("ul");
  const knowledge = state.activePackage.knowledge;
  const checksToShow = candidate.review_checks || [
    `${knowledge.hands_used} ${knowledge.hands_used === 1 ? "hand" : "hands"} expected`,
    `${knowledge.body_location} location`,
    index === 0 ? "Movement cue visible" : `${knowledge.expected_key_pose_count}-pose explanation`
  ];
  checksToShow.forEach((copy) => {
    const item = document.createElement("li");
    item.textContent = copy;
    checks.append(item);
  });
  body.append(top, title, note, checks);
  label.append(input, imageFrame, body);
  return label;
};

const renderVisualCandidates = () => {
  state.selectedCandidate = null;
  document.querySelector("#approve-visual").disabled = true;
  document.querySelector("#visual-candidates").replaceChildren(...state.currentCandidates.map(createCandidateCard));
  setText("#visual-review-status", "Select one visual option to continue.");
};

const showApprovedVisual = ({ persist = true, scroll = true } = {}) => {
  if (!state.selectedCandidate || !state.run || !state.activePackage) return;
  const approveButton = document.querySelector("#approve-visual");
  approveButton.disabled = true;
  approveButton.textContent = "Create family materials";
  document.querySelector("#regenerate-candidate").disabled = true;
  document.querySelectorAll('input[name="visual_candidate"]').forEach((input) => { input.disabled = true; });
  const visualState = document.querySelector("#visual-review-state");
  visualState.textContent = "Visual approved";
  visualState.className = "status-pill status-ready";
  const selectedIndex = state.currentCandidates.findIndex((candidate) => candidate.id === state.selectedCandidate.id);
  setText("#visual-review-status", `Option ${String.fromCharCode(65 + Math.max(0, selectedIndex))} approved. Choose the family material you want to create.`);
  setText("#content-status", "Create family materials");
  if (persist) {
    persistWorkflowRecord({
      candidate_ids: state.currentCandidates.map((candidate) => candidate.id),
      selected_candidate_id: state.selectedCandidate.id,
      visual_review_status: "APPROVED_FOR_INTERNAL_PRINTABLE",
      internal_printable_eligible: true
    });
    sessionStorage.setItem("kinderflowApprovedVisual", JSON.stringify({
      sign_id: state.activePackage.sign_id,
      cv_run_id: state.run.run_id,
      routine_context: state.run.sign.routine_context,
      candidate_id: state.selectedCandidate.id,
      asset: state.selectedCandidate.asset,
      content_hash: state.selectedCandidate.content_hash,
      status: "APPROVED_FOR_INTERNAL_PRINTABLE",
      internal_printable_eligible: true,
      publication_status: "DRAFT",
      source_run: state.run.run_id,
      approved_at: new Date().toISOString()
    }));
  }
  updateFamilyMaterialLinks();
  renderIllustrativeVideo();
  illustrativeMotionSection.hidden = false;
  downstreamSection.hidden = false;
  setProductStage(5);
  if (scroll) scrollToSection(illustrativeMotionSection);
};

document.querySelector("#generate-visual-candidates").addEventListener("click", (event) => {
  if (!state.currentCandidates.length && state.activePackage) {
    state.currentCandidates = [...state.activePackage.candidates];
  }
  event.currentTarget.disabled = true;
  event.currentTarget.textContent = "Creating visual options…";
  setText("#visual-preparation-status", "Creating visual options from the reviewed sign information…");
  window.setTimeout(() => {
    renderVisualCandidates();
    visualReviewSection.hidden = false;
    setText("#visual-preparation-status", "The visual options are ready for review.");
    event.currentTarget.textContent = "Visual options created";
    const visualState = document.querySelector("#visual-review-state");
    visualState.textContent = "Visual review";
    visualState.className = "status-pill status-review";
    persistWorkflowRecord({
      candidate_ids: state.currentCandidates.map((candidate) => candidate.id),
      visual_review_status: "REVIEW_REQUIRED",
      internal_printable_eligible: false
    });
    scrollToSection(visualReviewSection);
  }, 550);
});

document.querySelector("#regenerate-candidate").addEventListener("click", async (event) => {
  const button = event.currentTarget;
  button.disabled = true;
  button.textContent = "Creating visual option…";
  setText("#visual-review-status", "Creating a different local visual option…");
  try {
    const response = await fetch("/api/visual-candidates/regenerate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sign_id: state.activePackage.sign_id,
        existing_candidate_ids: state.currentCandidates.map((candidate) => candidate.id),
        evidence_route: state.evidenceRoute
      })
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "A new visual option could not be created.");
    const candidate = payload.candidate;
    const duplicates = state.currentCandidates.some((item) => item.id === candidate.id || item.asset === candidate.asset || item.content_hash === candidate.content_hash);
    if (duplicates) throw new Error("The new visual matched an existing option. The current options were kept.");
    state.currentCandidates.push(candidate);
    renderVisualCandidates();
    persistWorkflowRecord({
      candidate_ids: state.currentCandidates.map((item) => item.id),
      visual_review_status: "REVIEW_REQUIRED",
      internal_printable_eligible: false
    });
    setText("#visual-review-status", `A different visual option is ready. Select an option to continue.`);
    button.textContent = "Another visual option created";
  } catch (error) {
    setText("#visual-review-status", `${error.message} The current visual options were kept.`);
    button.disabled = false;
    button.textContent = "Create another visual option";
  }
});

document.querySelector("#approve-visual").addEventListener("click", (event) => {
  if (!state.selectedCandidate) return;
  showApprovedVisual();
});

document.querySelector("#reject-visual").addEventListener("click", () => {
  state.selectedCandidate = null;
  illustrativeMotionSection.hidden = true;
  clearIllustrativeVideo();
  downstreamSection.hidden = true;
  const approveVisual = document.querySelector("#approve-visual");
  approveVisual.disabled = true;
  approveVisual.textContent = "Approve selected visual";
  document.querySelector("#regenerate-candidate").disabled = false;
  document.querySelectorAll('input[name="visual_candidate"]').forEach((input) => {
    input.disabled = false;
    input.checked = false;
  });
  document.querySelectorAll(".visual-candidate-card").forEach((card) => card.classList.remove("is-selected"));
  sessionStorage.removeItem("kinderflowApprovedVisual");
  sessionStorage.removeItem("kinderflowPrintableApproval");
  const visualState = document.querySelector("#visual-review-state");
  visualState.textContent = "Visual review";
  visualState.className = "status-pill status-review";
  setText("#visual-review-status", "Visual rejected. Choose another option, create a different option, or choose a different pose.");
  setProductStage(4);
  persistWorkflowRecord({
    selected_candidate_id: null,
    visual_review_status: "REJECTED",
    internal_printable_eligible: false
  });
});

const resetToPoseSelection = () => {
  const frameInputs = [...document.querySelector("#suggested-reference-frames").querySelectorAll('input[type="checkbox"]')];
  frameInputs.forEach((input) => {
    input.checked = false;
    input.disabled = false;
  });
  state.selectedFrames = [];
  state.evidenceRoute = frameInputs.length
    ? "HUMAN_SELECTED_FRAME"
    : availableRouteForRun(state.run, state.activePackage);
  state.selectedCandidate = null;
  state.currentCandidates = [];
  illustrativeMotionSection.hidden = true;
  clearIllustrativeVideo();
  visualReviewSection.hidden = true;
  visualPreparationSection.hidden = true;
  downstreamSection.hidden = true;
  document.querySelector("#visual-candidates").replaceChildren();
  const generateButton = document.querySelector("#generate-visual-candidates");
  generateButton.disabled = false;
  generateButton.textContent = "Create visual options";
  const regenerateButton = document.querySelector("#regenerate-candidate");
  regenerateButton.disabled = false;
  regenerateButton.textContent = "Create another visual option";
  const approveVisualButton = document.querySelector("#approve-visual");
  approveVisualButton.disabled = true;
  approveVisualButton.textContent = "Approve selected visual";
  const approveReferenceButton = document.querySelector("#approve-sign");
  approveReferenceButton.hidden = false;
  approveReferenceButton.textContent = "Create family materials";
  document.querySelector("#use-another-reference").hidden = false;
  document.querySelectorAll('input[name="evidence_route"]').forEach((input) => {
    input.checked = input.value === state.evidenceRoute;
    input.disabled = (
      (input.value === "LANDMARK_KEY_POSE" && !trackedPosesAreAvailable(state.run))
      || (input.value === "HUMAN_SELECTED_FRAME" && frameInputs.length === 0)
    );
  });
  document.querySelector("#technical-review-rationale").disabled = false;
  sessionStorage.removeItem("kinderflowApprovedVisual");
  sessionStorage.removeItem("kinderflowPrintableApproval");
  persistWorkflowRecord({
    technical_review_action: null,
    technical_review_rationale: "",
    visual_evidence_route: state.evidenceRoute,
    selected_reference_frames: [],
    candidate_ids: [],
    selected_candidate_id: null,
    visual_review_status: "NOT_STARTED",
    internal_printable_eligible: false
  });
  updateEvidenceRouteUi();
  const reviewState = document.querySelector("#review-state");
  reviewState.textContent = "Reference review complete";
  reviewState.className = "status-pill status-ready";
  setText("#review-title", "Choose one or two reference poses");
  setText("#review-guidance", "Select the clearest moments to guide the visual.");
  setText("#review-message", "Choose a different pose. Your reference review is still complete.");
  setProductStage(3);
  scrollToSection(reviewSection);
};

document.querySelector("#choose-different-evidence").addEventListener("click", resetToPoseSelection);

document.querySelector("#use-another-reference").addEventListener("click", clearReference);

const checkService = async () => {
  renderStages();
  try {
    const response = await fetch("/api/health", { cache: "no-store" });
    if (!response.ok) throw new Error();
    serviceState.textContent = "Reference review ready";
  } catch {
    serviceState.textContent = "Reference review is unavailable";
    formMessage.textContent = "Start the local KinderFlow service, then reload this page.";
  }
};

const restoreWorkflowFromSession = async () => {
  const parameters = new URLSearchParams(window.location.search);
  if (parameters.get("restore") !== "1") return false;
  const workflow = readStoredPayload("kinderflowVisualWorkflow");
  const approvedVisual = readStoredPayload("kinderflowApprovedVisual");
  const runId = parameters.get("run") || workflow?.cv_run_id || approvedVisual?.cv_run_id;
  if (!workflow || !runId) throw new Error("The saved sign work could not be found. Use the reference review to continue.");
  let run = readStoredPayload("kinderflowReferenceReview");
  if (!run || run.run_id !== runId) {
    const response = await fetch(`/api/runs/${encodeURIComponent(runId)}`, { cache: "no-store" });
    if (!response.ok) throw new Error("The saved reference review is unavailable.");
    run = await response.json();
  }
  const runSignId = normalizeSignId(run.sign?.sign_id || run.sign?.name);
  if (workflow.cv_run_id !== runId
    || run.run_id !== runId
    || workflow.sign_id !== runSignId
    || !["complete", "failed", "insufficient_coverage"].includes(run.state)) {
    throw new Error("The saved sign work does not match this reference review.");
  }
  state.source = run.source?.kind === "demo_reference"
    ? "demo"
    : run.source?.kind === "direct_video_url"
      ? "url"
      : "upload";
  state.inputMode = state.source === "url" ? "url" : "upload";
  state.run = run;
  signControl.value = run.sign.name;
  signControl.disabled = true;
  document.querySelector("#routine-context").value = run.sign.routine_context;
  directVideoInput.value = state.source === "url" ? run.source?.reference_source_url || "" : "";
  fileName.textContent = run.source?.display_filename || `${run.sign.name} reference video`;
  fileMeta.textContent = "Saved reference review";
  document.querySelector("#direct-video-meta").textContent = "Saved direct-video reference review";
  syncReferenceInputMode(state.inputMode, { clearSelection: false });
  form.querySelectorAll("input, select, button").forEach((control) => { control.disabled = true; });
  retryButton.disabled = false;
  state.workflowRecord = workflow;
  finishRun(run, { scroll: false });
  state.evidenceRoute = availableRouteForRun(run, state.activePackage, workflow.visual_evidence_route);
  document.querySelectorAll('input[name="evidence_route"]').forEach((input) => {
    input.checked = input.value === state.evidenceRoute;
  });
  const selectedFrames = new Set(workflow.selected_reference_frames || []);
  document.querySelector("#suggested-reference-frames").querySelectorAll('input[type="checkbox"]').forEach((input) => {
    input.checked = selectedFrames.has(input.value);
  });
  document.querySelector("#technical-review-rationale").value = workflow.technical_review_rationale || "";
  updateEvidenceRouteUi();
  if (run.state !== "complete" || !["Pass", "Review needed"].includes(run.technical_status)) return true;
  const restoredFrames = [...state.selectedFrames];
  const expectedReviewAction = state.evidenceRoute === "KNOWLEDGE_REFERENCE_FALLBACK"
    ? "ACCEPT_WITH_FALLBACK"
    : "ACCEPT_FOR_VISUAL_PREPARATION";
  const restoredDecisionIsValid = workflow.technical_review_action === expectedReviewAction
    && SUPPORTED_SIGN_IDS.has(runSignId)
    && visualPackageIsReady(state.activePackage)
    && evidenceRouteIsAvailable(state.evidenceRoute, run)
    && (state.evidenceRoute !== "HUMAN_SELECTED_FRAME" || (restoredFrames.length >= 1 && restoredFrames.length <= 2))
    && (state.evidenceRoute !== "KNOWLEDGE_REFERENCE_FALLBACK"
      || Boolean(document.querySelector("#technical-review-rationale").value.trim()));
  if (!restoredDecisionIsValid) {
    const hasDerivedVisualState = Boolean(workflow.technical_review_action)
      || ["READY_TO_GENERATE", "REVIEW_REQUIRED", "REJECTED", "APPROVED_FOR_INTERNAL_PRINTABLE"].includes(
        workflow.visual_review_status
      )
      || Boolean(approvedVisual);
    if (hasDerivedVisualState) {
      state.selectedCandidate = null;
      state.currentCandidates = [];
      state.selectedFrames = [];
      document.querySelector("#suggested-reference-frames").querySelectorAll('input[type="checkbox"]').forEach((input) => {
        input.checked = false;
        input.disabled = false;
      });
      document.querySelector("#technical-review-rationale").value = "";
      document.querySelector("#technical-review-rationale").disabled = false;
      document.querySelectorAll('input[name="evidence_route"]').forEach((input) => {
        input.checked = input.value === state.evidenceRoute;
        input.disabled = (
          (input.value === "LANDMARK_KEY_POSE" && !trackedPosesAreAvailable(run))
          || (input.value === "HUMAN_SELECTED_FRAME" && !(run.artifacts?.suggested_reference_frames || []).length)
        );
      });
      sessionStorage.removeItem("kinderflowApprovedVisual");
      sessionStorage.removeItem("kinderflowPrintableApproval");
      persistWorkflowRecord({
        technical_review_action: null,
        technical_review_rationale: "",
        selected_reference_frames: [],
        candidate_ids: [],
        selected_candidate_id: null,
        visual_review_status: "NOT_STARTED",
        internal_printable_eligible: false
      });
      updateEvidenceRouteUi();
    }
    return true;
  }
  markReferenceReviewComplete();
  document.querySelector("#approve-sign").disabled = true;
  document.querySelector("#approve-sign").textContent = "Pose choice saved";
  document.querySelector("#use-another-reference").hidden = true;
  renderVisualPreparation();
  illustrativeMotionSection.hidden = true;
  visualPreparationSection.hidden = false;
  setProductStage(4);
  const visualWasGenerated = ["REVIEW_REQUIRED", "REJECTED", "APPROVED_FOR_INTERNAL_PRINTABLE"].includes(
    workflow.visual_review_status
  );
  const candidateIds = new Set(workflow.candidate_ids || []);
  state.currentCandidates = visualWasGenerated
    ? allPackageCandidates().filter((candidate) => candidateIds.has(candidate.id))
    : [];
  if (!state.currentCandidates.length && visualWasGenerated) {
    state.currentCandidates = [...state.activePackage.candidates];
  }
  if (visualWasGenerated && state.currentCandidates.length) {
    renderVisualCandidates();
    visualReviewSection.hidden = false;
  }
  if (approvedVisual
    && approvedVisual.status === "APPROVED_FOR_INTERNAL_PRINTABLE"
    && approvedVisual.internal_printable_eligible === true
    && approvedVisual.publication_status === "DRAFT"
    && workflow.visual_review_status === "APPROVED_FOR_INTERNAL_PRINTABLE"
    && workflow.internal_printable_eligible === true
    && workflow.publication_status === "DRAFT"
    && approvedVisual.sign_id === state.activePackage.sign_id
    && approvedVisual.cv_run_id === run.run_id
    && workflow.selected_candidate_id === approvedVisual.candidate_id) {
    state.selectedCandidate = allPackageCandidates().find((candidate) => (
      candidate.id === approvedVisual.candidate_id
      && candidate.asset === approvedVisual.asset
      && Boolean(approvedVisual.content_hash)
      && candidate.content_hash === approvedVisual.content_hash
    )) || null;
    if (state.selectedCandidate) {
      const selectedInput = document.querySelector(`input[name="visual_candidate"][value="${state.selectedCandidate.id}"]`);
      if (selectedInput) {
        selectedInput.checked = true;
        selectedInput.closest(".visual-candidate-card")?.classList.add("is-selected");
      }
      showApprovedVisual({ persist: false, scroll: false });
    }
  }
  const view = parameters.get("view");
  const target = view === "family-materials" && !illustrativeMotionSection.hidden
    ? illustrativeMotionSection
    : visualReviewSection.hidden ? reviewSection : visualReviewSection;
  scrollToSection(target);
  return true;
};

document.querySelector("#continue-to-family-materials").addEventListener("click", () => {
  scrollToSection(downstreamSection);
});

syncReferenceInputMode("upload", { clearSelection: false });
setProductStage(1);

Promise.allSettled([loadVisualPackages(), loadIllustrativeVideoCatalog(), checkService()]).then(async (results) => {
  const packageResult = results[0];
  if (packageResult.status === "rejected") {
    formMessage.textContent = `${packageResult.reason.message} Reload this page to try again.`;
    return;
  }
  try {
    await restoreWorkflowFromSession();
  } catch (error) {
    formMessage.textContent = error.message;
  }
});
