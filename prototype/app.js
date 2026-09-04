"use strict";

const FAMILY_SIGNS = {
  more: {
    en: "MORE",
    es: "MÁS",
    routine: "Snack time · Playtime",
    image: "assets/signs/more-a.svg",
    materials: ["video", "flashcard", "routine-card", "story"],
    when: "Use MORE during snack time, mealtime or play when your child wants an activity or moment to continue.",
    tryIt: "Say “more” while showing the familiar sign, then pause and respond to your child’s cues.",
    storyTitle: "A little more?",
    story: "Lina asks for more during snack time. Her family says the word, shows the familiar sign and keeps the moment relaxed."
  },
  help: {
    en: "HELP",
    es: "AYUDA",
    routine: "Getting ready",
    image: "assets/signs/help-a.svg",
    materials: ["video", "flashcard", "routine-card"],
    when: "Use HELP when a familiar task feels tricky, such as getting dressed or putting toys away.",
    tryIt: "Say “help” while showing the sign, then offer calm support and time to respond."
  },
  milk: {
    en: "MILK",
    es: "LECHE",
    routine: "Milk time",
    image: "assets/signs/milk-a.svg",
    materials: ["video", "flashcard", "routine-card"],
    when: "Use MILK when preparing or offering your child’s usual milk drink.",
    tryIt: "Say “milk” while showing the sign just before the familiar drink appears."
  },
  eat: {
    en: "EAT",
    es: "COMER",
    routine: "Mealtime",
    image: "assets/signs/eat-a.svg",
    materials: ["flashcard", "routine-card"],
    when: "Use EAT as mealtime begins or when talking about food during a familiar routine.",
    tryIt: "Say “eat” while showing the sign, then continue the meal without asking for repetition."
  },
  sleep: {
    en: "SLEEP",
    es: "DORMIR",
    routine: "Bedtime",
    image: "assets/signs/sleep-a.svg",
    materials: ["flashcard", "routine-card"],
    when: "Use SLEEP during the calm, familiar steps that lead into a nap or bedtime.",
    tryIt: "Say “sleep” while showing the sign as you move through your usual bedtime routine."
  },
  water: {
    en: "WATER",
    es: "AGUA",
    routine: "Drink break",
    image: "assets/signs/water-a.svg",
    materials: ["flashcard", "routine-card"],
    when: "Use WATER when offering a drink at meals, after play or during another familiar break.",
    tryIt: "Say “water” while showing the sign, then offer the drink and follow your child’s interest."
  }
};

const MATERIAL_LABELS = {
  video: "Video tutorial",
  flashcard: "Flashcard",
  "routine-card": "Routine Card",
  story: "Story"
};
const MATERIAL_ORDER = Object.keys(MATERIAL_LABELS);
const GROUPS = {
  "Group 0–1": ["Child A", "Child B"],
  "Group 1–2": ["Child C", "Child D"],
  "Group 2–3": ["Child E", "Child F"]
};
const DEFAULT_ASSIGNMENTS = [{
  id: "seed-more-babies",
  signId: "more",
  groupId: "Group 0–1",
  audienceType: "group",
  childId: "",
  materials: ["video", "flashcard"],
  routineContext: "Snack time · Playtime",
  illustrativeVideoAvailable: true
}];
const DEFAULT_CONTEXT = {
  assignmentId: "seed-more-babies",
  groupId: "Group 0–1",
  audienceType: "group",
  childId: ""
};

const signList = document.querySelector("#family-sign-list");
const status = document.querySelector("#family-library-status");
const emptyState = document.querySelector("#family-empty-state");
const demoNote = document.querySelector("#family-demo-note");
const detailSection = document.querySelector("#family-materials");
const detailCard = document.querySelector("#family-sign-detail");
const videoMaterial = document.querySelector("#family-video-material");
const materialSummary = document.querySelector("#family-detail-materials");
const flashcardMaterial = document.querySelector("#family-flashcard-material");
const routineMaterial = document.querySelector("#family-routine-material");
const storyMaterial = document.querySelector("#family-story-material");

const storageAvailable = typeof sessionStorage !== "undefined";
const readSessionJSON = (key) => {
  if (!storageAvailable) return null;
  try {
    return JSON.parse(sessionStorage.getItem(key) || "null");
  } catch (_error) {
    return null;
  }
};

const safeMaterials = (signId, values) => {
  const available = FAMILY_SIGNS[signId]?.materials || [];
  return [...new Set(Array.isArray(values) ? values : [])]
    .filter((material) => MATERIAL_ORDER.includes(material) && available.includes(material))
    .sort((left, right) => MATERIAL_ORDER.indexOf(left) - MATERIAL_ORDER.indexOf(right));
};

const safeAssignment = (value) => {
  const signId = String(value?.signId || "").toLowerCase();
  const groupId = String(value?.groupId || "");
  const audienceType = value?.audienceType === "child" ? "child" : value?.audienceType === "group" ? "group" : "";
  const childId = audienceType === "child" ? String(value?.childId || "") : "";
  const materials = safeMaterials(signId, value?.materials);
  if (!FAMILY_SIGNS[signId]
    || !GROUPS[groupId]
    || !audienceType
    || (audienceType === "child" && !GROUPS[groupId].includes(childId))
    || !materials.length) return null;
  return {
    id: String(value?.id || ""),
    signId,
    groupId,
    audienceType,
    childId,
    materials,
    routineContext: String(value?.routineContext || "").slice(0, 180),
    illustrativeVideoAvailable: value?.illustrativeVideoAvailable === true
  };
};

const readAssignments = () => {
  if (!storageAvailable) return { assignments: DEFAULT_ASSIGNMENTS.map((item) => ({ ...item })), fallback: true };
  const raw = sessionStorage.getItem("kinderflowSchoolAssignments");
  if (raw === null) return { assignments: DEFAULT_ASSIGNMENTS.map((item) => ({ ...item })), fallback: true };
  try {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return { assignments: DEFAULT_ASSIGNMENTS.map((item) => ({ ...item })), fallback: true };
    return { assignments: parsed.map(safeAssignment).filter(Boolean), fallback: false };
  } catch (_error) {
    return { assignments: DEFAULT_ASSIGNMENTS.map((item) => ({ ...item })), fallback: true };
  }
};

const readFamilyContext = (fallback, assignments, requestedSign) => {
  const stored = readSessionJSON("kinderflowFamilyPreviewAssignmentId");
  if (stored && GROUPS[stored.groupId] && ["group", "child"].includes(stored.audienceType)) {
    const childId = stored.audienceType === "child" && GROUPS[stored.groupId].includes(stored.childId)
      ? stored.childId
      : "";
    if (stored.audienceType === "group" || childId) {
      return {
        assignmentId: String(stored.assignmentId || ""),
        groupId: stored.groupId,
        audienceType: stored.audienceType,
        childId
      };
    }
  }
  if (fallback) return { ...DEFAULT_CONTEXT };
  const selected = assignments.find((assignment) => assignment.signId === requestedSign) || assignments[0];
  return selected ? {
    assignmentId: selected.id,
    groupId: selected.groupId,
    audienceType: selected.audienceType,
    childId: selected.childId
  } : null;
};

const belongsToFamily = (assignment, context) => {
  if (!context) return true;
  if (assignment.groupId !== context.groupId) return false;
  if (context.audienceType === "group") return assignment.audienceType === "group";
  return assignment.audienceType === "group"
    || (assignment.audienceType === "child" && assignment.childId === context.childId);
};

const combineSigns = (assignments) => {
  const combined = new Map();
  assignments.forEach((assignment) => {
    const current = combined.get(assignment.signId) || {
      signId: assignment.signId,
      materials: [],
      routineContext: ""
    };
    current.materials = safeMaterials(assignment.signId, [...current.materials, ...assignment.materials]);
    if (!current.routineContext && assignment.routineContext) current.routineContext = assignment.routineContext;
    combined.set(assignment.signId, current);
  });
  return [...combined.values()];
};

const createChip = (label) => {
  const chip = document.createElement("span");
  chip.className = "material-chip";
  chip.textContent = label;
  return chip;
};

const renderLibraryCard = (item) => {
  const sign = FAMILY_SIGNS[item.signId];
  const article = document.createElement("article");
  article.className = "family-library-card";
  article.dataset.familySign = item.signId;
  const image = document.createElement("img");
  image.src = sign.image;
  image.alt = `${sign.en} sign illustration`;
  const copy = document.createElement("div");
  copy.className = "family-library-copy";
  const title = document.createElement("h3");
  title.textContent = `${sign.en} / ${sign.es}`;
  const routine = document.createElement("p");
  routine.className = "family-library-routine";
  routine.textContent = item.routineContext || sign.routine;
  const chips = document.createElement("div");
  chips.className = "family-library-materials";
  chips.setAttribute("aria-label", "Shared materials");
  item.materials.forEach((material) => chips.append(createChip(MATERIAL_LABELS[material])));
  const open = document.createElement("button");
  open.type = "button";
  open.className = "button button-primary";
  open.dataset.openFamilySign = item.signId;
  open.textContent = `Open ${sign.en}`;
  copy.append(title, routine, chips, open);
  article.append(image, copy);
  return article;
};

const renderUnavailableVideo = () => {
  videoMaterial.replaceChildren();
  const heading = document.createElement("h3");
  heading.textContent = "Baby Sign video tutorial";
  const message = document.createElement("p");
  message.textContent = "Video tutorial not available yet. Use the Flashcard or Routine Card instead.";
  videoMaterial.append(heading, message);
};

const renderVideoLoading = () => {
  videoMaterial.replaceChildren();
  const heading = document.createElement("h3");
  heading.textContent = "Baby Sign video tutorial";
  const message = document.createElement("p");
  message.textContent = "Loading family materials…";
  videoMaterial.append(heading, message);
};

const normalizeVideoCatalog = (payload) => {
  if (payload?.signs && !Array.isArray(payload.signs)) return payload.signs;
  if (Array.isArray(payload?.signs)) return Object.fromEntries(payload.signs.map((record) => [record.sign_id, record]));
  return {};
};

let videoCatalogPromise;
const getVideoCatalog = () => {
  if (!videoCatalogPromise) {
    videoCatalogPromise = fetch("/api/illustrative-videos", { cache: "no-store" })
      .then((response) => {
        if (!response.ok) throw new Error("Video catalogue unavailable");
        return response.json();
      })
      .then(normalizeVideoCatalog)
      .catch(() => ({}));
  }
  return videoCatalogPromise;
};

const renderVideo = async (signId, renderToken) => {
  renderVideoLoading();
  const catalog = await getVideoCatalog();
  if (videoMaterial.dataset.renderToken !== renderToken) return;
  const record = catalog[signId];
  if (!record?.available || !record?.url) {
    renderUnavailableVideo();
    return;
  }
  videoMaterial.replaceChildren();
  const heading = document.createElement("h3");
  heading.textContent = "Baby Sign video tutorial";
  const copy = document.createElement("p");
  copy.textContent = "Watch the movement together, then use the sign naturally in your routine.";
  const video = document.createElement("video");
  video.controls = true;
  video.playsInline = true;
  video.preload = "metadata";
  video.src = record.url;
  video.setAttribute("aria-label", `${FAMILY_SIGNS[signId].en} Baby Sign video tutorial`);
  video.addEventListener("error", () => {
    if (videoMaterial.dataset.renderToken === renderToken) renderUnavailableVideo();
  }, { once: true });
  videoMaterial.append(heading, copy, video);
};

const showSign = (item) => {
  const sign = FAMILY_SIGNS[item.signId];
  document.querySelector("#family-detail-title").textContent = `${sign.en} / ${sign.es}`;
  document.querySelector("#family-detail-routine").textContent = item.routineContext || sign.routine;
  document.querySelector("#family-when-copy").textContent = sign.when;
  document.querySelector("#family-try-copy").textContent = sign.tryIt;
  materialSummary.replaceChildren(...item.materials.map((material) => createChip(MATERIAL_LABELS[material])));

  const hasVideo = item.materials.includes("video");
  videoMaterial.hidden = !hasVideo;
  const renderToken = `${item.signId}-${Date.now()}`;
  videoMaterial.dataset.renderToken = renderToken;
  if (hasVideo) renderVideo(item.signId, renderToken);
  else videoMaterial.replaceChildren();

  flashcardMaterial.hidden = !item.materials.includes("flashcard");
  routineMaterial.hidden = !item.materials.includes("routine-card");
  storyMaterial.hidden = !item.materials.includes("story");
  const signImage = document.querySelector("#family-sign-image");
  signImage.src = sign.image;
  signImage.alt = `${sign.en} sign illustration`;
  document.querySelector("#family-routine-copy").textContent = `Use ${sign.en} naturally during ${String(item.routineContext || sign.routine).toLowerCase()}.`;
  document.querySelector("#family-story-title").textContent = sign.storyTitle || `${sign.en} together`;
  storyMaterial.querySelector("p:last-child").textContent = sign.story || `A short family story using ${sign.en} in a familiar routine.`;

  detailSection.hidden = false;
  detailCard.focus({ preventScroll: true });
  detailSection.scrollIntoView({ behavior: window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ? "auto" : "smooth", block: "start" });
};

const initialiseFamilyLibrary = () => {
  const source = readAssignments();
  const requestedSign = String(new URLSearchParams(window.location.search).get("sign") || "").toLowerCase();
  const context = readFamilyContext(source.fallback, source.assignments, requestedSign);
  const visibleSigns = combineSigns(source.assignments.filter((assignment) => belongsToFamily(assignment, context)));
  demoNote.hidden = !source.fallback;
  signList.replaceChildren(...visibleSigns.map(renderLibraryCard));
  emptyState.hidden = visibleSigns.length !== 0;
  status.textContent = visibleSigns.length
    ? `${visibleSigns.length} ${visibleSigns.length === 1 ? "sign" : "signs"} shared with your family.`
    : "No active signs to show.";

  signList.addEventListener("click", (event) => {
    const button = event.target.closest("[data-open-family-sign]");
    if (!button) return;
    const item = visibleSigns.find((value) => value.signId === button.dataset.openFamilySign);
    if (item) showSign(item);
  });

  const initial = visibleSigns.find((item) => item.signId === requestedSign);
  if (initial) {
    const requestedCard = signList.querySelector(`[data-family-sign="${initial.signId}"]`);
    requestedCard?.classList.add("is-requested");
    requestedCard?.querySelector("[data-open-family-sign]")?.focus();
  }
};

document.querySelector("#print-family-card")?.addEventListener("click", () => window.print());
if (signList) initialiseFamilyLibrary();
