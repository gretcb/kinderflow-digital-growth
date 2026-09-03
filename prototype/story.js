"use strict";

const ROUTINES = {
  snack: {
    en: { label: "Snack time", title: "A little more?", opening: "Lina finished her pieces of pear.", continuation: "snack time" },
    es: { label: "Hora de la merienda", title: "¿Un poco más?", opening: "Lina terminó sus trozos de pera.", continuation: "la merienda" }
  },
  bedtime: {
    en: { label: "Bedtime", title: "One more story", opening: "Lina was enjoying bedtime.", continuation: "bedtime" },
    es: { label: "Hora de dormir", title: "Un cuento más", opening: "Lina se preparaba para dormir.", continuation: "la rutina de dormir" }
  },
  dressing: {
    en: { label: "Getting dressed", title: "One more sock", opening: "Lina was getting dressed.", continuation: "getting dressed" },
    es: { label: "Vestirse", title: "Un calcetín más", opening: "Lina se estaba vistiendo.", continuation: "la rutina de vestirse" }
  },
  playtime: {
    en: { label: "Playtime", title: "One more piece", opening: "Lina was enjoying playtime.", continuation: "playtime" },
    es: { label: "Hora de jugar", title: "Una pieza más", opening: "Lina estaba jugando.", continuation: "el juego" }
  }
};

const LANGUAGE_COPY = {
  en: {
    label: "English", sign: "MORE",
    middle: {
      calm: "She looked at Dad and used the MORE sign.",
      playful: "She looked at Dad, smiled and used the MORE sign.",
      reassuring: "She looked calmly at Dad and used the MORE sign."
    },
    shortEnding: "“Would you like more?” Dad asked. Lina smiled and Dad repeated the MORE sign.",
    longEnding: (continuation) => `“Would you like more?” Dad asked. Lina smiled. Dad continued ${continuation} and repeated the MORE sign. They finished the routine without rushing.`,
    attribution: "Story for shared reading",
    draftPrompt: "Create the draft to preview the complete story in English."
  },
  es: {
    label: "Spanish", sign: "MÁS",
    middle: {
      calm: "Miró a papá e hizo el signo MÁS.",
      playful: "Miró a papá, sonrió e hizo el signo MÁS.",
      reassuring: "Miró tranquilamente a papá e hizo el signo MÁS."
    },
    shortEnding: "«¿Quieres más?», preguntó papá. Lina sonrió y papá repitió el signo MÁS.",
    longEnding: (continuation) => `«¿Quieres más?», preguntó papá. Lina sonrió. Papá continuó con ${continuation} y repitió el signo MÁS. Terminaron la rutina sin prisas.`,
    attribution: "Cuento para leer en familia",
    draftPrompt: "Crea el borrador para ver el cuento completo en español."
  }
};

const form = document.querySelector("#story-form");
const preview = document.querySelector("#story-preview");
const heading = document.querySelector("#story-heading");
const body = document.querySelector("#story-body");
const meta = document.querySelector("#story-meta");
const attribution = document.querySelector("#story-attribution");
const stateLabel = document.querySelector("#story-state");
const wordCount = document.querySelector("#word-count");
const languageCheck = document.querySelector("#story-language-check");
const routineCheck = document.querySelector("#story-routine-check");
const signCheck = document.querySelector("#story-sign-check");
const reviewStatus = document.querySelector("#story-review-status");
const approveButton = document.querySelector("#approve-story");
const requestChangesButton = document.querySelector("#request-story-changes");
const keepDraftButton = document.querySelector("#keep-story-draft");
const storySign = document.querySelector("#story-sign");
const storySubmitButton = document.querySelector('#story-form button[type="submit"]');
const steps = Array.from(document.querySelectorAll("[data-story-step]"));
const checkResults = Array.from(document.querySelectorAll("#evaluation-list .check-result"));
let storySourceApproved = false;

const setState = (state, label) => {
  stateLabel.textContent = label;
  stateLabel.className = `status-pill ${state === "published" ? "status-ready" : "status-review"}`;
  const order = ["draft", "evaluation", "review", "published"];
  const activeIndex = order.indexOf(state);
  steps.forEach((step) => {
    const stepIndex = order.indexOf(step.dataset.storyStep);
    step.classList.toggle("is-complete", stepIndex < activeIndex);
    step.classList.toggle("is-current", stepIndex === activeIndex);
  });
};

const setReviewControls = (enabled) => {
  approveButton.disabled = !enabled;
  requestChangesButton.disabled = !enabled;
  keepDraftButton.disabled = !enabled;
};

const normalizeRequestedSign = (value) => String(value || "")
  .trim()
  .toLowerCase()
  .replaceAll(/[^a-z0-9]+/g, "_")
  .replaceAll(/^_+|_+$/g, "");

const requestedSignLabel = (signId) => signId
  ? signId.replaceAll("_", " ").toUpperCase()
  : "REQUESTED SIGN";

const storySignIsAvailable = () => storySourceApproved && storySign?.value === "more";

const previewAttribution = () => LANGUAGE_COPY[document.querySelector("#story-language")?.value]?.attribution
  || LANGUAGE_COPY.en.attribution;

const renderMissingVisualApproval = (signId) => {
  const label = requestedSignLabel(signId || "more");
  heading.textContent = "Complete the visual review first";
  body.textContent = "Approve the sign visual before creating a story from it.";
  attribution.textContent = previewAttribution();
  meta.textContent = `${label} · Story not started`;
  checkResults.forEach((result) => {
    result.textContent = "WAITING";
    result.className = "check-result review";
  });
  signCheck.textContent = "Waiting for an approved sign visual";
  routineCheck.textContent = "Waiting for an approved sign visual";
  languageCheck.textContent = "Waiting for an approved sign visual";
  wordCount.textContent = "No story was created";
  reviewStatus.textContent = "Return to the visual options and approve a sign visual to continue.";
  setState("draft", "Visual approval needed");
  setReviewControls(false);
  if (storySubmitButton) storySubmitButton.disabled = true;
};

const renderUnavailableStorySign = (signId) => {
  const label = requestedSignLabel(signId);
  heading.textContent = "Story unavailable for this sign";
  body.textContent = "A story has not been prepared for this sign yet.";
  attribution.textContent = previewAttribution();
  meta.textContent = `${label} · Not available`;
  checkResults.forEach((result) => {
    result.textContent = "WAITING";
    result.className = "check-result review";
  });
  signCheck.textContent = "Choose MORE to create a story draft";
  routineCheck.textContent = "Waiting for an available sign";
  languageCheck.textContent = "Waiting for an available sign";
  wordCount.textContent = "No story was created";
  reviewStatus.textContent = "Choose a sign with a prepared Story to continue.";
  setState("draft", "Not available");
  setReviewControls(false);
  if (storySubmitButton) storySubmitButton.disabled = true;
  storySign?.setAttribute("aria-invalid", "true");
};

const selectRequestedStorySign = (signId) => {
  if (!storySign || signId === "more") return;
  const option = document.createElement("option");
  option.value = signId;
  option.textContent = `${requestedSignLabel(signId)} — Not available`;
  option.dataset.unsupportedSign = "true";
  storySign.append(option);
  storySign.value = signId;
};

const buildStory = ({ routine, length, tone, language }) => {
  const languageCopy = LANGUAGE_COPY[language] || LANGUAGE_COPY.en;
  const context = ROUTINES[routine]?.[language] || ROUTINES.snack[language] || ROUTINES.snack.en;
  const ending = length === "very-short" ? languageCopy.shortEnding : languageCopy.longEnding(context.continuation);
  return {
    context, languageCopy, title: context.title,
    text: `${context.opening} ${languageCopy.middle[tone] || languageCopy.middle.calm} ${ending}`
  };
};

const renderChecks = ({ story, values, count }) => {
  checkResults.forEach((result, index) => {
    result.textContent = index < 6 ? "PASS" : "REVIEW";
    result.className = `check-result ${index < 6 ? "pass" : "review"}`;
  });
  signCheck.textContent = `${story.languageCopy.sign} appears in the story`;
  routineCheck.textContent = `${story.context.label} is reflected in the story`;
  languageCheck.textContent = `Matches ${story.languageCopy.label} selection`;
  wordCount.textContent = `${count} words · ${values.length === "very-short" ? "very-short" : "short"} limit met`;
};

const renderDraft = (values) => {
  const story = buildStory(values);
  heading.textContent = story.title;
  body.textContent = story.text;
  attribution.textContent = story.languageCopy.attribution;
  meta.textContent = `${story.languageCopy.sign} · ${story.context.label} · ${values.age} · ${story.languageCopy.label}`;
  const count = story.text.trim().split(/\s+/).length;
  renderChecks({ story, values, count });
  reviewStatus.textContent = "Checks complete. Draft is ready for human review.";
  setState("review", "Ready for human review");
  setReviewControls(true);
};

const resetDraftForChangedBrief = () => {
  if (!storySourceApproved) {
    renderMissingVisualApproval(storySign?.value || "");
    return;
  }
  if (!storySignIsAvailable()) {
    renderUnavailableStorySign(storySign?.value || "");
    return;
  }
  storySign?.querySelector('option[data-unsupported-sign="true"]')?.remove();
  storySign?.removeAttribute("aria-invalid");
  if (storySubmitButton) storySubmitButton.disabled = false;
  const values = Object.fromEntries(new FormData(form));
  const languageCopy = LANGUAGE_COPY[values.language] || LANGUAGE_COPY.en;
  const context = ROUTINES[values.routine]?.[values.language] || ROUTINES.snack[values.language] || ROUTINES.snack.en;
  heading.textContent = "Story preview";
  body.textContent = languageCopy.draftPrompt;
  attribution.textContent = languageCopy.attribution;
  meta.textContent = `${languageCopy.sign} · ${context.label} · ${values.age} · ${languageCopy.label}`;
  checkResults.forEach((result) => {
    result.textContent = "WAITING";
    result.className = "check-result review";
  });
  signCheck.textContent = "Create a new draft to check the selected sign";
  routineCheck.textContent = "Create a new draft to check the routine";
  languageCheck.textContent = `${languageCopy.label} selected`;
  wordCount.textContent = "Create a new draft to check the length";
  reviewStatus.textContent = "Story details changed. Create a new draft before review.";
  setState("draft", "Create a new draft");
  setReviewControls(false);
};

form?.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!storySignIsAvailable()) {
    renderUnavailableStorySign(storySign?.value || "");
    return;
  }
  renderDraft(Object.fromEntries(new FormData(form)));
  preview.focus();
});

form?.addEventListener("change", resetDraftForChangedBrief);

approveButton?.addEventListener("click", () => {
  setState("published", "Approved locally");
  reviewStatus.textContent = "Approved in this demo. Nothing was sent or added to the library.";
});

requestChangesButton?.addEventListener("click", () => {
  setState("review", "Changes requested");
  reviewStatus.textContent = "Changes requested. The draft has not been added to the library.";
});

keepDraftButton?.addEventListener("click", () => {
  setState("draft", "Draft");
  reviewStatus.textContent = "Kept as a local draft. Nothing was sent or added to the library.";
});

if (typeof window !== "undefined") {
  const parameters = new URLSearchParams(window.location.search);
  const readStoredPayload = (key) => {
    try {
      return JSON.parse(sessionStorage.getItem(key) || "null");
    } catch (_error) {
      return null;
    }
  };
  const approvedVisual = readStoredPayload("kinderflowApprovedVisual");
  const workflow = readStoredPayload("kinderflowVisualWorkflow");
  const requestedSign = normalizeRequestedSign(parameters.get("sign") || approvedVisual?.sign_id || "more");
  storySourceApproved = parameters.get("approved") === "1"
    && approvedVisual?.status === "APPROVED_FOR_INTERNAL_PRINTABLE"
    && approvedVisual?.internal_printable_eligible === true
    && approvedVisual?.publication_status === "DRAFT"
    && approvedVisual?.sign_id === requestedSign
    && workflow?.sign_id === requestedSign
    && workflow?.cv_run_id === approvedVisual.cv_run_id
    && workflow?.selected_candidate_id === approvedVisual.candidate_id
    && workflow?.visual_review_status === "APPROVED_FOR_INTERNAL_PRINTABLE"
    && (!parameters.get("source_run") || parameters.get("source_run") === approvedVisual.cv_run_id)
    && (!parameters.get("visual") || parameters.get("visual") === approvedVisual.candidate_id);
  const requestedRoutine = String(parameters.get("routine") || "").trim().toLowerCase();
  if (requestedRoutine) {
    const routineControl = document.querySelector("#story-routine");
    const routineKey = Object.keys(ROUTINES).find((key) => (
      requestedRoutine.includes(ROUTINES[key].en.label.toLowerCase())
      || requestedRoutine.includes(key)
    ));
    if (routineKey) routineControl.value = routineKey;
  }
  const returnLink = document.querySelector("#back-to-family-materials-story");
  const sourceRun = parameters.get("source_run") || workflow?.cv_run_id;
  returnLink.href = sourceRun
    ? `create-sign.html?${new URLSearchParams({ restore: "1", view: "family-materials", run: sourceRun }).toString()}`
    : "create-sign.html";
  if (!storySourceApproved) {
    if (requestedSign !== "more") selectRequestedStorySign(requestedSign);
    renderMissingVisualApproval(requestedSign);
  } else if (parameters.has("sign")) {
    if (requestedSign !== "more") {
      selectRequestedStorySign(requestedSign);
      renderUnavailableStorySign(requestedSign);
    } else if (requestedRoutine) {
      resetDraftForChangedBrief();
    }
  } else if (requestedRoutine) {
    resetDraftForChangedBrief();
  }
}
