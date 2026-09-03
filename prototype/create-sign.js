"use strict";

const STAGES = [
  ["video_received", "Video received"],
  ["video_validation", "Video validation"],
  ["landmark_extraction", "Landmark extraction"],
  ["movement_normalization", "Movement normalization"],
  ["motion_analysis", "Motion analysis"],
  ["technical_checks", "Technical checks"],
  ["results_ready", "Results ready"]
];

const state = {
  source: null,
  file: null,
  run: null,
  polling: null,
  visualPackages: [],
  activePackage: null,
  selectedCandidate: null,
  currentCandidates: [],
  evidenceRoute: null,
  selectedFrames: [],
  workflowRecord: null
};
const form = document.querySelector("#sign-run-form");
const fileInput = document.querySelector("#reference-video");
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
const visualPreparationSection = document.querySelector("#visual-preparation-section");
const visualReviewSection = document.querySelector("#visual-review-section");
const downstreamSection = document.querySelector("#downstream-section");

const escapeQuery = (value) => encodeURIComponent(value || "");

const renderStages = (stages = STAGES.map(([key, label]) => ({ key, label, status: "Waiting" }))) => {
  stageList.replaceChildren(...stages.map((stage, index) => {
    const item = document.createElement("li");
    item.dataset.status = stage.status.toLowerCase().replaceAll(" ", "-");
    const number = document.createElement("span");
    number.textContent = String(index + 1).padStart(2, "0");
    const label = document.createElement("strong");
    label.textContent = stage.label;
    const status = document.createElement("small");
    status.textContent = stage.status;
    item.append(number, label, status);
    return item;
  }));
};

const setSelectedSource = (source, selectedFile = null) => {
  state.source = source;
  state.file = selectedFile;
  runButton.disabled = false;
  if (source === "demo") {
    fileName.textContent = "sign_reference.mp4";
    fileMeta.textContent = "Demo reference · stored locally · 573 KB";
    formMessage.textContent = "Demo reference selected. Ready to run the real movement check.";
  }
};

const resetRun = () => {
  if (state.polling) window.clearTimeout(state.polling);
  state.run = null;
  resultSection.hidden = true;
  reviewSection.hidden = true;
  visualPreparationSection.hidden = true;
  visualReviewSection.hidden = true;
  downstreamSection.hidden = true;
  state.activePackage = null;
  state.selectedCandidate = null;
  state.currentCandidates = [];
  state.evidenceRoute = null;
  state.selectedFrames = [];
  state.workflowRecord = null;
  document.querySelector("#visual-candidates").replaceChildren();
  const generateButton = document.querySelector("#generate-visual-candidates");
  generateButton.disabled = false;
  generateButton.textContent = "Generate visual candidates";
  const regenerateButton = document.querySelector("#regenerate-candidate");
  regenerateButton.disabled = false;
  const approveVisualButton = document.querySelector("#approve-visual");
  approveVisualButton.disabled = true;
  approveVisualButton.textContent = "Approve selected visual";
  retryButton.hidden = true;
  const approve = document.querySelector("#approve-sign");
  approve.hidden = false;
  approve.disabled = false;
  approve.textContent = "Prepare visual";
  document.querySelector("#use-another-reference").hidden = false;
  const reviewState = document.querySelector("#review-state");
  reviewState.textContent = "Technical review needed";
  reviewState.className = "status-pill status-review";
  setText("#review-message", "No technical review action recorded.");
  document.querySelector("#technical-review-rationale").value = "";
  document.querySelector("#suggested-reference-frames").replaceChildren();
  form.querySelectorAll("input, select, button").forEach((control) => { control.disabled = false; });
  runButton.disabled = !state.source;
  renderStages();
  processingNote.textContent = state.source ? "Reference selected. Ready to run." : "Waiting for a reference video.";
  formMessage.textContent = state.source ? "Ready to run the movement check." : "Select an MP4 or use the demo reference.";
};

const clearReference = () => {
  resetRun();
  state.source = null;
  state.file = null;
  fileInput.value = "";
  fileName.textContent = "No video selected";
  fileMeta.textContent = "MP4 · maximum 100 MB";
  runButton.disabled = true;
  formMessage.textContent = "Select an MP4 or use the demo reference.";
  document.querySelector(".create-sign-setup").scrollIntoView({ behavior: "smooth", block: "start" });
};

const formatBytes = (bytes) => bytes < 1024 * 1024
  ? `${Math.max(1, Math.round(bytes / 1024))} KB`
  : `${(bytes / 1024 / 1024).toFixed(1)} MB`;

fileInput.addEventListener("change", () => {
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
  formMessage.textContent = "Reference video selected. Ready to run the movement check.";
});

document.querySelector("#use-demo-video").addEventListener("click", () => setSelectedSource("demo"));
retryButton.addEventListener("click", resetRun);

const requestRun = async () => {
  const signName = document.querySelector("#sign-name").value.trim();
  const routineContext = document.querySelector("#routine-context").value.trim();
  const referenceStatus = document.querySelector("#reference-status").value;
  const referenceSourceUrl = document.querySelector("#reference-source-url").value.trim();
  if (!signName || !routineContext) throw new Error("Complete the sign name and routine before processing.");
  if (!state.source) throw new Error("Select an MP4 or use the demo reference.");

  if (state.source === "demo") {
    return fetch("/api/runs/demo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sign_name: signName, routine_context: routineContext, reference_status: referenceStatus, reference_source_url: referenceSourceUrl })
    });
  }
  const payload = new FormData();
  payload.append("sign_name", signName);
  payload.append("routine_context", routineContext);
  payload.append("reference_status", referenceStatus);
  payload.append("reference_source_url", referenceSourceUrl);
  payload.append("reference_video", state.file);
  return fetch("/api/runs/upload", { method: "POST", body: payload });
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  runButton.disabled = true;
  retryButton.hidden = true;
  resultSection.hidden = true;
  reviewSection.hidden = true;
  visualPreparationSection.hidden = true;
  visualReviewSection.hidden = true;
  downstreamSection.hidden = true;
  formMessage.textContent = "Sending the local reference to the movement pipeline…";
  processingNote.textContent = "Starting the movement check. Processing may take about a minute.";
  renderStages(STAGES.map(([key, label], index) => ({ key, label, status: index === 0 ? "Running" : "Waiting" })));
  document.querySelector("#processing-section").scrollIntoView({ behavior: "smooth", block: "start" });
  try {
    const response = await requestRun();
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "The movement check could not be started.");
    state.run = payload;
    form.querySelectorAll("input, select, button").forEach((control) => { control.disabled = true; });
    retryButton.disabled = false;
    formMessage.textContent = `Run started: ${payload.run_id}`;
    pollRun(payload.run_id);
  } catch (error) {
    formMessage.textContent = error.message;
    processingNote.textContent = "The movement check could not be started.";
    retryButton.hidden = false;
    retryButton.disabled = false;
  }
});

const pollRun = async (runId) => {
  try {
    const response = await fetch(`/api/runs/${encodeURIComponent(runId)}`, { cache: "no-store" });
    if (!response.ok) throw new Error("Run status is unavailable.");
    const run = await response.json();
    state.run = run;
    renderStages(run.stages);
    const active = run.stages.find((stage) => stage.status === "Running");
    processingNote.textContent = active ? `${active.label} is running locally…` : `Run state: ${run.state.replaceAll("_", " ")}.`;
    if (["complete", "failed", "insufficient_coverage"].includes(run.state)) {
      finishRun(run);
      return;
    }
    state.polling = window.setTimeout(() => pollRun(runId), 900);
  } catch (error) {
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

const loadVisualPackages = async () => {
  const response = await fetch("data/visual_sign_packages.json", { cache: "no-store" });
  if (!response.ok) throw new Error("Visual sign packages are unavailable.");
  const payload = await response.json();
  if (!Array.isArray(payload.signs)) throw new Error("Visual sign packages are invalid.");
  state.visualPackages = payload.signs;
};

const ROUTE_COPY = {
  LANDMARK_KEY_POSE: {
    level: 1, title: "Landmark key poses", note: "Curated sign knowledge + MediaPipe key poses + functional sign reference.", status: "Usable"
  },
  HUMAN_SELECTED_FRAME: {
    level: 2, title: "Human-selected reference frame", note: "Curated sign knowledge + operator-selected reference poses + functional sign reference.", status: "Human selection"
  },
  KNOWLEDGE_REFERENCE_FALLBACK: {
    level: 3, title: "Knowledge and sign-reference fallback", note: "Curated sign mechanics + functional sign reference + any usable movement evidence.", status: "Grounded fallback"
  },
  INTERNAL_POSE_GUIDE: {
    level: 4, title: "Internal pose guide", note: "Controlled Open Peeps pose guide — not final artwork.", status: "Review required"
  }
};

const routeForRun = (run, signPackage) => {
  if (!signPackage) return null;
  if (run.technical_status === "Pass") return signPackage.evidence_routes.pass;
  if (run.technical_status === "Review needed") return signPackage.evidence_routes.review;
  return signPackage.evidence_routes.fallback;
};

const routeCopy = () => ROUTE_COPY[state.evidenceRoute] || ROUTE_COPY.KNOWLEDGE_REFERENCE_FALLBACK;

const persistWorkflowRecord = (updates = {}) => {
  const now = new Date().toISOString();
  const base = state.workflowRecord || {
    sign_id: state.activePackage?.sign_id || normalizeSignId(state.run?.sign?.name),
    cv_run_id: state.run?.run_id || null,
    technical_status: (state.run?.technical_status || "Waiting").toUpperCase().replaceAll(" ", "_"),
    technical_review_action: null,
    technical_review_rationale: "",
    visual_evidence_route: state.evidenceRoute,
    candidate_ids: state.currentCandidates.map((candidate) => candidate.id),
    selected_candidate_id: null,
    visual_review_status: "NOT_STARTED",
    internal_printable_eligible: false,
    publication_status: "DRAFT",
    last_updated: now
  };
  state.workflowRecord = { ...base, ...updates, publication_status: "DRAFT", last_updated: now };
  sessionStorage.setItem("kinderflowVisualWorkflow", JSON.stringify(state.workflowRecord));
};

const updateEvidenceRouteUi = () => {
  const route = state.evidenceRoute;
  const isFrames = route === "HUMAN_SELECTED_FRAME";
  const isFallback = route === "KNOWLEDGE_REFERENCE_FALLBACK";
  document.querySelector("#reference-frame-picker").hidden = !isFrames;
  document.querySelector("#fallback-rationale-field").hidden = !isFallback;
  setText("#source-detail-route", ROUTE_COPY[route]?.title || "Not selected");
  const action = document.querySelector("#approve-sign");
  action.textContent = isFallback
    ? "Continue with grounded fallback"
    : `Prepare ${state.activePackage?.labels?.en || "sign"} visual`;
  setText("#review-message", isFallback
    ? "Add a concise rationale before continuing. This accepts technical evidence only; visual review is still required."
    : "Choose the clearest available evidence route, then prepare the visual.");
};

const renderSuggestedFrames = (frames = []) => {
  state.selectedFrames = [];
  const container = document.querySelector("#suggested-reference-frames");
  if (!frames.length) {
    container.replaceChildren();
    setText("#frame-picker-help", "Suggested frames are unavailable. Choose grounded fallback or use another video.");
    return;
  }
  container.replaceChildren(...frames.slice(0, 6).map((frame) => {
    const label = document.createElement("label");
    const input = document.createElement("input");
    input.type = "checkbox";
    input.value = frame.id;
    input.addEventListener("change", () => {
      if (input.checked && state.selectedFrames.length >= 2) {
        input.checked = false;
        setText("#frame-picker-help", "Choose no more than two poses.");
        return;
      }
      state.selectedFrames = [...container.querySelectorAll("input:checked")].map((item) => item.value);
      setText("#frame-picker-help", state.selectedFrames.length ? `${state.selectedFrames.length} pose${state.selectedFrames.length > 1 ? "s" : ""} selected.` : "Select at least one frame.");
    });
    const image = document.createElement("img");
    image.src = frame.url;
    image.alt = `${frame.label}, suggested still from the validated reference video`;
    const text = document.createElement("span");
    text.textContent = frame.label;
    label.append(input, image, text);
    return label;
  }));
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

const finishRun = (run) => {
  retryButton.hidden = false;
  retryButton.disabled = false;
  formMessage.textContent = run.state === "complete" ? "Movement check complete." : run.error?.message || "Movement check finished with limited evidence.";
  const isComplete = run.state === "complete";
  state.activePackage = state.visualPackages.find((item) => item.sign_id === normalizeSignId(run.sign?.name));
  state.evidenceRoute = routeForRun(run, state.activePackage);
  state.currentCandidates = state.activePackage ? [...state.activePackage.candidates] : [];
  const canPrepare = Boolean(state.activePackage);
  const hasMetrics = Boolean(run.metrics);
  const hasArtifacts = Boolean(run.artifacts && run.artifacts.reference_video_url);
  const explanations = {
    "Pass": "Technical capture is sufficient to prepare a review candidate.",
    "Review needed": "The run produced usable evidence with conditions. Review it before preparing the visual.",
    "Fail": "Movement evidence is not sufficient for landmark conditioning. A visual package, when available, is a separate grounded fallback."
  };
  setText("#result-kicker", "Movement check complete");
  setText("#result-title", run.technical_status);
  setText("#result-explanation", explanations[run.technical_status] || run.error?.message || "The movement check could not be completed.");
  processingNote.textContent = isComplete
    ? "Results ready. Review the summary and visual evidence below."
    : run.error?.message || "The movement check could not be completed.";
  setText("#technical-status", run.technical_status);
  setText("#content-status", canPrepare ? "Visual package available" : "Visual package unavailable");
  setText("#run-identifier", "Movement run recorded");
  setText("#source-detail-run", run.run_id);
  const sourceUrl = run.source?.reference_source_url;
  const sourceDetail = document.querySelector("#source-detail-url");
  sourceDetail.replaceChildren();
  if (sourceUrl) {
    const link = document.createElement("a");
    link.href = sourceUrl;
    link.target = "_blank";
    link.rel = "noopener";
    link.textContent = "Open reference webpage";
    sourceDetail.append(link);
  } else {
    sourceDetail.textContent = "Not provided";
  }
  document.querySelector("#movement-comparison").hidden = !hasArtifacts;
  document.querySelector("#technical-details").hidden = !hasMetrics;
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
        document.querySelector("#movement-video-preview"),
        document.querySelector("#movement-playback-status"),
        run.artifacts.movement_preview_url,
        run.run_id
      );
    }
    if (run.artifacts.detection_timeline_url) {
      const timeline = document.querySelector("#detection-timeline");
      timeline.src = run.artifacts.detection_timeline_url;
      document.querySelector("#detection-timeline-link").href = run.artifacts.detection_timeline_url;
    }
    if (run.artifacts.wrist_trajectory_url) {
      const wrist = document.querySelector("#wrist-trajectory");
      wrist.src = run.artifacts.wrist_trajectory_url;
      document.querySelector("#wrist-trajectory-link").href = run.artifacts.wrist_trajectory_url;
    }
  }
  renderSuggestedFrames(run.artifacts?.suggested_reference_frames || []);
  const warnings = run.warnings.length ? run.warnings : ["No additional technical warnings were recorded."];
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
  reviewReasons.replaceChildren(...warnings.map((warning) => {
    const item = document.createElement("li");
    item.textContent = warning;
    return item;
  }));
  reviewReasons.hidden = run.technical_status === "Pass";
  const approveButton = document.querySelector("#approve-sign");
  approveButton.hidden = !canPrepare;
  approveButton.textContent = state.activePackage ? `Prepare ${state.activePackage.labels.en} visual` : "Prepare visual";
  const reviewHeadings = {
    "Pass": "Ready to prepare visual",
    "Review needed": state.activePackage?.sign_id === "eat" ? "Technical review needed — usable with grounded fallback" : "Technical review needed",
    "Fail": "Movement evidence needs fallback"
  };
  const reviewGuidance = {
    "Pass": "Review the movement evidence, then prepare a grounded visual candidate.",
    "Review needed": state.activePackage?.sign_id === "eat"
      ? "Important movement evidence is available, but some hand tracking is incomplete near the face. Continue with the grounded sign reference and available movement evidence, or use another reference video."
      : "Review the conditions below, choose reference poses, then prepare the visual or use another reference.",
    "Fail": "The movement evidence is blocked. If a grounded package is available, use fallback explicitly; otherwise use another reference."
  };
  setText("#review-title", reviewHeadings[run.technical_status] || "Review movement evidence");
  setText("#review-guidance", canPrepare
    ? reviewGuidance[run.technical_status] || "Review the evidence before preparing a visual."
    : "No local visual package matches this sign yet. Use another sign or add a reviewed package.");
  const reviewState = document.querySelector("#review-state");
  reviewState.textContent = run.technical_status === "Pass" ? "Ready to prepare visual" : "Technical review needed";
  reviewState.className = `status-pill ${run.technical_status === "Pass" ? "status-ready" : "status-review"}`;
  resultSection.hidden = false;
  reviewSection.hidden = false;
  document.querySelectorAll('input[name="evidence_route"]').forEach((input) => {
    input.checked = input.value === state.evidenceRoute;
    input.disabled = (
      (input.value === "LANDMARK_KEY_POSE" && run.technical_status !== "Pass")
      || (input.value === "HUMAN_SELECTED_FRAME" && !(run.artifacts?.suggested_reference_frames || []).length)
    );
  });
  persistWorkflowRecord();
  updateEvidenceRouteUi();
  resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
};

const renderVisualPreparation = () => {
  const signPackage = state.activePackage;
  const route = routeCopy();
  document.querySelectorAll("[data-active-sign]").forEach((element) => { element.textContent = signPackage.labels.en; });
  setText("#grounding-source", signPackage.grounding_sources[0].label);
  setText("#grounding-source-note", signPackage.grounding_sources[0].role);
  setText("#grounding-source-status", signPackage.grounding_sources[0].status === "Applied" ? "Applied" : "Review");
  setText("#grounding-motion", route.title);
  setText("#grounding-motion-note", route.note);
  setText("#grounding-motion-status", route.status);
  document.querySelector("#grounding-motion-status").className = `grounding-status ${route.level === 1 ? "status-ready" : "status-review"}`;
  setText("#grounding-character", signPackage.visual_identity.base_system);
  setText("#grounding-character-note", signPackage.visual_identity.operator_description);
  setText("#visual-brief-title", `${signPackage.movement.hands} ${signPackage.movement.hands === 1 ? "hand" : "hands"} · ${signPackage.movement.body_location.toLowerCase()} · ${signPackage.knowledge.direction.toLowerCase()} movement`);
  setText("#visual-brief-description", `${signPackage.movement.description} ${signPackage.movement.presentation}`);
  setText("#fallback-title", `Evidence route ${route.level}`);
  setText("#fallback-description", route.note);
  setText("#visual-preparation-status", "Ready to create two grounded vector candidates for human review.");
};

document.querySelectorAll('input[name="evidence_route"]').forEach((input) => {
  input.addEventListener("change", () => {
    state.evidenceRoute = input.value;
    updateEvidenceRouteUi();
    persistWorkflowRecord({ visual_evidence_route: state.evidenceRoute });
  });
});

document.querySelector("#approve-sign").addEventListener("click", (event) => {
  if (!state.activePackage) return;
  if (state.evidenceRoute === "HUMAN_SELECTED_FRAME" && !state.selectedFrames.length) {
    setText("#review-message", "Choose at least one suggested reference pose before preparing the visual.");
    document.querySelector("#reference-frame-picker").scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }
  const rationale = document.querySelector("#technical-review-rationale").value.trim();
  if (state.evidenceRoute === "KNOWLEDGE_REFERENCE_FALLBACK" && !rationale) {
    setText("#review-message", "Add a short technical-review rationale for grounded fallback.");
    document.querySelector("#technical-review-rationale").focus();
    return;
  }
  const action = state.evidenceRoute === "KNOWLEDGE_REFERENCE_FALLBACK" ? "ACCEPT_WITH_FALLBACK" : "ACCEPT_FOR_VISUAL_PREPARATION";
  persistWorkflowRecord({
    technical_review_action: action,
    technical_review_rationale: rationale || `Operator selected ${routeCopy().title.toLowerCase()} after reviewing movement evidence.`,
    visual_evidence_route: state.evidenceRoute,
    selected_reference_frames: [...state.selectedFrames],
    visual_review_status: "READY_TO_GENERATE",
    internal_printable_eligible: false
  });
  event.currentTarget.disabled = true;
  event.currentTarget.textContent = "Evidence reviewed";
  document.querySelector("#use-another-reference").hidden = true;
  const reviewState = document.querySelector("#review-state");
  reviewState.textContent = "Ready to prepare visual";
  reviewState.className = "status-pill status-ready";
  setText("#content-status", "Ready to prepare visual");
  setText("#result-kicker", "Technical review recorded locally");
  setText("#result-title", "Ready to prepare visual");
  setText("#review-title", "Movement review recorded");
  setText("#review-guidance", "The evidence route is resolved. Prepare the visual using the grounded sign package.");
  setText("#review-message", "Current technical evidence accepted for visual preparation only. Human visual review is still required; no sign certification or publication was created.");
  renderVisualPreparation();
  visualPreparationSection.hidden = false;
  visualPreparationSection.scrollIntoView({ behavior: "smooth", block: "start" });
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
    setText("#visual-review-status", `${candidate.label} selected. Check the hands and movement cue, then approve the visual.`);
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
  badge.textContent = candidate.label;
  const recommendation = document.createElement("span");
  recommendation.className = "candidate-recommendation";
  recommendation.textContent = `Best for ${candidate.recommended_for.toLowerCase()}`;
  top.append(badge, recommendation);
  const title = document.createElement("h3");
  title.textContent = candidate.title;
  const note = document.createElement("p");
  note.textContent = candidate.review_note;
  const checks = document.createElement("ul");
  const knowledge = state.activePackage.knowledge;
  [
    `${knowledge.hands_used} ${knowledge.hands_used === 1 ? "hand" : "hands"} expected`,
    `${knowledge.body_location} location`,
    index === 0 ? "Movement cue visible" : `${knowledge.expected_key_pose_count}-pose explanation`
  ].forEach((copy) => {
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
  setText("#visual-review-status", "Select one candidate to continue.");
};

document.querySelector("#generate-visual-candidates").addEventListener("click", (event) => {
  event.currentTarget.disabled = true;
  event.currentTarget.textContent = "Generating visual…";
  setText("#visual-preparation-status", "Generating visual candidates from the resolved sign package…");
  window.setTimeout(() => {
    renderVisualCandidates();
    visualReviewSection.hidden = false;
    setText("#visual-preparation-status", "Two controlled candidates are ready for visual review.");
    event.currentTarget.textContent = "Candidates generated";
    const visualState = document.querySelector("#visual-review-state");
    visualState.textContent = "Visual review";
    visualState.className = "status-pill status-review";
    persistWorkflowRecord({
      candidate_ids: state.currentCandidates.map((candidate) => candidate.id),
      visual_review_status: "REVIEW_REQUIRED",
      internal_printable_eligible: false
    });
    visualReviewSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 550);
});

document.querySelector("#regenerate-candidate").addEventListener("click", async (event) => {
  const button = event.currentTarget;
  button.disabled = true;
  button.textContent = "Generating candidate…";
  setText("#visual-review-status", "Building a distinct local vector recomposition…");
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
    if (!response.ok) throw new Error(payload.error || "A new candidate could not be generated.");
    const candidate = payload.candidate;
    const duplicates = state.currentCandidates.some((item) => item.id === candidate.id || item.asset === candidate.asset || item.content_hash === candidate.content_hash);
    if (duplicates) throw new Error("The candidate service returned a duplicate. Existing candidates were kept.");
    state.currentCandidates.push(candidate);
    renderVisualCandidates();
    persistWorkflowRecord({
      candidate_ids: state.currentCandidates.map((item) => item.id),
      visual_review_status: "REVIEW_REQUIRED",
      internal_printable_eligible: false
    });
    setText("#visual-review-status", `${candidate.label} created with a new ID, asset version and vector content. Select a candidate to continue.`);
    button.textContent = "Another candidate generated";
  } catch (error) {
    setText("#visual-review-status", `${error.message} Existing candidates were kept.`);
    button.disabled = false;
    button.textContent = "Generate another candidate";
  }
});

document.querySelector("#approve-visual").addEventListener("click", (event) => {
  if (!state.selectedCandidate) return;
  event.currentTarget.disabled = true;
  event.currentTarget.textContent = "Approved for internal printable";
  document.querySelector("#regenerate-candidate").disabled = true;
  document.querySelectorAll('input[name="visual_candidate"]').forEach((input) => { input.disabled = true; });
  const visualState = document.querySelector("#visual-review-state");
  visualState.textContent = "Approved for internal printable";
  visualState.className = "status-pill status-ready";
  setText("#visual-review-status", `${state.selectedCandidate.label} approved by the operator for an internal printable.`);
  setText("#content-status", "Approved for internal printable");
  persistWorkflowRecord({
    candidate_ids: state.currentCandidates.map((candidate) => candidate.id),
    selected_candidate_id: state.selectedCandidate.id,
    visual_review_status: "APPROVED_FOR_INTERNAL_PRINTABLE",
    internal_printable_eligible: true
  });
  sessionStorage.setItem("kinderflowApprovedVisual", JSON.stringify({
    sign_id: state.activePackage.sign_id,
    cv_run_id: state.run.run_id,
    candidate_id: state.selectedCandidate.id,
    asset: state.selectedCandidate.asset,
    content_hash: state.selectedCandidate.content_hash,
    status: "APPROVED_FOR_INTERNAL_PRINTABLE",
    internal_printable_eligible: true,
    publication_status: "DRAFT",
    source_run: state.run.run_id,
    approved_at: new Date().toISOString()
  }));
  const sign = state.run.sign;
  const query = `?sign=${escapeQuery(sign.name)}&routine=${escapeQuery(sign.routine_context)}&source_run=${escapeQuery(state.run.run_id)}`;
  document.querySelector("#continue-content-engine-link").href = `library.html${query}#content-engine-title`;
  document.querySelector("#create-story-link").href = `create-story.html${query}`;
  document.querySelector("#create-printable-link").href = `flashcards.html?sign=${escapeQuery(sign.name)}&visual=${escapeQuery(state.selectedCandidate.id)}&approved=1`;
  downstreamSection.hidden = false;
  downstreamSection.scrollIntoView({ behavior: "smooth", block: "start" });
});

document.querySelector("#reject-visual").addEventListener("click", () => {
  state.selectedCandidate = null;
  downstreamSection.hidden = true;
  document.querySelector("#approve-visual").disabled = true;
  const visualState = document.querySelector("#visual-review-state");
  visualState.textContent = "Visual review required";
  visualState.className = "status-pill status-review";
  setText("#visual-review-status", "Visual rejected. Generate another candidate, choose different pose evidence, or use another reference video.");
  persistWorkflowRecord({
    selected_candidate_id: null,
    visual_review_status: "REJECTED",
    internal_printable_eligible: false
  });
});

document.querySelector("#choose-different-evidence").addEventListener("click", () => {
  visualReviewSection.hidden = true;
  visualPreparationSection.hidden = true;
  const approveButton = document.querySelector("#approve-sign");
  approveButton.disabled = false;
  approveButton.textContent = state.evidenceRoute === "KNOWLEDGE_REFERENCE_FALLBACK" ? "Continue with grounded fallback" : `Prepare ${state.activePackage.labels.en} visual`;
  setText("#review-message", "Choose another evidence route or pose selection, then prepare the visual again.");
  reviewSection.scrollIntoView({ behavior: "smooth", block: "start" });
});

document.querySelector("#use-another-reference").addEventListener("click", clearReference);

const checkService = async () => {
  renderStages();
  try {
    const response = await fetch("/api/health", { cache: "no-store" });
    if (!response.ok) throw new Error();
    serviceState.textContent = "Local movement service ready";
  } catch {
    serviceState.textContent = "Start the local MVP service to process video";
    formMessage.textContent = "Run “python mvp/app.py” from the repository root, then reopen this page at localhost:8000.";
  }
};

Promise.allSettled([loadVisualPackages(), checkService()]).then((results) => {
  const packageResult = results[0];
  if (packageResult.status === "rejected") {
    formMessage.textContent = `${packageResult.reason.message} Serve the prototype through the local MVP service and reload.`;
  }
});
