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

const state = { source: null, file: null, run: null, polling: null };
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
  downstreamSection.hidden = true;
  retryButton.hidden = true;
  const approve = document.querySelector("#approve-sign");
  approve.hidden = false;
  approve.disabled = false;
  approve.textContent = "Approve";
  document.querySelector("#use-another-reference").hidden = false;
  const reviewState = document.querySelector("#review-state");
  reviewState.textContent = "Draft";
  reviewState.className = "status-pill status-review";
  setText("#review-message", "No approval action recorded.");
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
  if (!signName || !routineContext) throw new Error("Complete the sign name and routine before processing.");
  if (!state.source) throw new Error("Select an MP4 or use the demo reference.");

  if (state.source === "demo") {
    return fetch("/api/runs/demo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sign_name: signName, routine_context: routineContext, reference_status: referenceStatus })
    });
  }
  const payload = new FormData();
  payload.append("sign_name", signName);
  payload.append("routine_context", routineContext);
  payload.append("reference_status", referenceStatus);
  payload.append("reference_video", state.file);
  return fetch("/api/runs/upload", { method: "POST", body: payload });
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  runButton.disabled = true;
  retryButton.hidden = true;
  resultSection.hidden = true;
  reviewSection.hidden = true;
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
  formMessage.textContent = run.state === "complete" ? "Movement check complete." : run.error.message;
  const isComplete = run.state === "complete";
  const canApprove = isComplete && ["Pass", "Review needed"].includes(run.technical_status);
  const hasMetrics = Boolean(run.metrics);
  const hasArtifacts = Boolean(run.artifacts && run.artifacts.reference_video_url);
  const explanations = {
    "Pass": "Technical capture is sufficient for review.",
    "Review needed": "The run produced usable movement data, but technical issues should be reviewed before approval.",
    "Fail": "The reference does not provide sufficient technical movement data."
  };
  setText("#result-kicker", "Movement check complete");
  setText("#result-title", run.technical_status);
  setText("#result-explanation", explanations[run.technical_status] || run.error?.message || "The movement check could not be completed.");
  processingNote.textContent = isComplete
    ? "Results ready. Review the summary and visual evidence below."
    : run.error?.message || "The movement check could not be completed.";
  setText("#technical-status", run.technical_status);
  setText("#content-status", run.content_status);
  setText("#run-identifier", `Run ${run.run_id}`);
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
    loadRunVideo(
      document.querySelector("#movement-video-preview"),
      document.querySelector("#movement-playback-status"),
      run.artifacts.movement_preview_url,
      run.run_id
    );
    const timeline = document.querySelector("#detection-timeline");
    timeline.src = run.artifacts.detection_timeline_url;
    document.querySelector("#detection-timeline-link").href = run.artifacts.detection_timeline_url;
    const wrist = document.querySelector("#wrist-trajectory");
    wrist.src = run.artifacts.wrist_trajectory_url;
    document.querySelector("#wrist-trajectory-link").href = run.artifacts.wrist_trajectory_url;
  }
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
  approveButton.hidden = !canApprove;
  approveButton.textContent = run.technical_status === "Review needed" ? "Approve anyway" : "Approve";
  const reviewHeadings = {
    "Pass": "Approve this sign",
    "Review needed": "Review technical notes",
    "Fail": "Use another reference video"
  };
  const reviewGuidance = {
    "Pass": "The technical capture is sufficient. Human approval remains the publication decision.",
    "Review needed": "Review the reasons below, then approve anyway or use another reference.",
    "Fail": "Approval is unavailable because the technical capture failed."
  };
  setText("#review-title", reviewHeadings[run.technical_status] || "Movement check could not be completed");
  setText("#review-guidance", reviewGuidance[run.technical_status] || "Use another reference video.");
  resultSection.hidden = false;
  reviewSection.hidden = false;
  resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
};

document.querySelector("#approve-sign").addEventListener("click", (event) => {
  event.currentTarget.disabled = true;
  event.currentTarget.textContent = "Review recorded";
  document.querySelector("#use-another-reference").hidden = true;
  const reviewState = document.querySelector("#review-state");
  reviewState.textContent = "Approved locally";
  reviewState.className = "status-pill status-ready";
  setText("#content-status", "Ready for content preparation");
  setText("#result-kicker", "Human review recorded locally");
  setText("#result-title", "Ready for content preparation");
  setText("#review-title", "Movement review recorded");
  setText("#review-guidance", "Continue to the Content Engine. Final library publication remains a separate controlled decision.");
  setText("#review-message", "Local browser state only. No production approval or publication record was created.");
  const sign = state.run.sign;
  const query = `?sign=${escapeQuery(sign.name)}&routine=${escapeQuery(sign.routine_context)}&source_run=${escapeQuery(state.run.run_id)}`;
  document.querySelector("#continue-content-engine-link").href = `library.html${query}#content-engine-title`;
  document.querySelector("#create-story-link").href = `create-story.html${query}`;
  downstreamSection.hidden = false;
  downstreamSection.scrollIntoView({ behavior: "smooth", block: "start" });
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

checkService();
