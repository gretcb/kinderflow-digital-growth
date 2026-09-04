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
  en: {
    language: "Bilingual",
    routine: "Routine",
    guidance: "How to use it",
    context: "Everyday context",
    missingContext: "Context image not prepared yet",
    cardKinds: { flashcard: "FLASHCARD", routine: "ROUTINE CARD" }
  },
  es: {
    language: "Spanish",
    routine: "Rutina",
    guidance: "Cómo usarlo",
    context: "Contexto cotidiano",
    missingContext: "Imagen de contexto aún no preparada",
    cardKinds: { flashcard: "TARJETA DIDÁCTICA", routine: "TARJETA DE RUTINA" }
  }
};

const KNOWN_ROUTINES_ES = {
  "snack time": "Hora de la merienda",
  "playtime": "Hora de jugar",
  "mealtime": "Hora de comer",
  "getting ready": "Prepararse",
  "getting dressed": "Vestirse",
  "bedtime": "Hora de dormir",
  "milk time": "Hora de la leche",
  "drink break": "Pausa para beber",
  "drinks": "Bebidas",
  "end of a meal": "Fin de una comida",
  "activity": "Actividad"
};

const MOVEMENT_COPY = {
  more: { en: "MEET · SEPARATE · REPEAT", es: "JUNTAR · SEPARAR · REPETIR" },
  help: { en: "SUPPORTED · MOVE UP", es: "APOYAR · SUBIR" },
  eat: { en: "START · END", es: "INICIO · FINAL" },
  sleep: { en: "SPREAD · GATHER BELOW CHIN", es: "ABRIR · JUNTAR BAJO LA BARBILLA" },
  milk: { en: "OPEN · CLOSE · REPEAT IN PLACE", es: "ABRIR · CERRAR · REPETIR EN EL MISMO LUGAR" },
  water: { en: "START · END", es: "INICIO · FINAL" }
};

const ILLUSTRATIVE_VIDEO_SIGNS = new Set(["more", "help", "milk"]);

const SVG_TEXT_ES = {
  "START": "INICIO",
  "END": "FINAL",
  "MEET · SEPARATE · REPEAT": "JUNTAR · SEPARAR · REPETIR",
  "OPEN · CLOSE · REPEAT IN PLACE": "ABRIR · CERRAR · REPETIR",
  "BESIDE THE LOWER FACE": "JUNTO AL ROSTRO",
  "IN FRONT OF THE FACE TO BELOW THE CHIN": "DEL ROSTRO A BAJO LA BARBILLA",
  "IN FRONT OF THE UPPER TORSO": "DELANTE DEL TORSO",
  "UPPER CHEST": "PECHO",
  "MOUTH": "BOCA",
  "SUPPORTED · MOVE UP": "APOYAR · SUBIR",
  "SPREAD · GATHER BELOW CHIN": "ABRIR · JUNTAR BAJO LA BARBILLA",
  "THREE FINGERS · LOWER FACE": "TRES DEDOS · ROSTRO",
  "ONE REVIEWED TAP · MOUTH": "UN TOQUE REVISADO · BOCA",
  "MORE · MÁS": "MÁS",
  "HELP · AYUDA": "AYUDA",
  "EAT · COMER": "COMER",
  "SLEEP · DORMIR": "DORMIR",
  "MILK · LECHE": "LECHE",
  "WATER · AGUA": "AGUA",
  "Inward": "Hacia dentro",
  "Upward": "Hacia arriba",
  "Downward": "Hacia abajo",
  "Toward the mouth": "Hacia la boca",
  "Toward the lower face": "Hacia el rostro",
  "Open and closed in place": "Abrir y cerrar en el sitio",
  "DRAFT · HUMAN REVIEW REQUIRED": "BORRADOR · REVISIÓN HUMANA",
  "Inward · DRAFT · HUMAN REVIEW REQUIRED": "HACIA DENTRO · REVISIÓN HUMANA",
  "Upward · DRAFT · HUMAN REVIEW REQUIRED": "HACIA ARRIBA · REVISIÓN HUMANA",
  "Downward · DRAFT · HUMAN REVIEW REQUIRED": "HACIA ABAJO · REVISIÓN HUMANA",
  "Toward the mouth · DRAFT · HUMAN REVIEW REQUIRED": "HACIA LA BOCA · REVISIÓN HUMANA",
  "Toward the lower face · DRAFT · HUMAN REVIEW REQUIRED": "HACIA EL ROSTRO · REVISIÓN HUMANA",
  "Open and closed in place · DRAFT · HUMAN REVIEW REQUIRED": "ABRIR Y CERRAR · REVISIÓN HUMANA"
};

const builder = {
  signs: [], selectedId: null, language: "en", cardType: "flashcard",
  layoutReviewed: false, reviewedHandoff: null, visualPackages: [], approvedVisual: null,
  activeCandidate: null, unsupportedRequest: null, requestedRoutine: null,
  requestedSignId: null, printableApproval: null, routineContext: null,
  familyGuidance: null, printablePreferences: null, renderRevision: 0
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

const readStoredPayload = (key) => {
  try {
    return JSON.parse(sessionStorage.getItem(key) || "null");
  } catch (_error) {
    return null;
  }
};

const hasBilingualCopy = (value) => Boolean(
  String(value?.en || "").trim()
  && String(value?.es || "").trim()
);

const localizeRoutineContext = (value) => {
  const routine = String(value || "").trim();
  if (!routine) return "";
  const pieces = routine.split(/(\s*(?:,|\/)\s*)/);
  let fullyLocalized = true;
  const localized = pieces.map((piece, index) => {
    if (index % 2 !== 0) return piece;
    const normalized = piece.trim().toLowerCase();
    const translated = KNOWN_ROUTINES_ES[normalized];
    if (!translated) fullyLocalized = false;
    return translated || "";
  }).join("");
  return fullyLocalized ? localized : "";
};

const normalizeRoutineContext = (value, fallback) => {
  const fallbackEnglish = String(fallback?.en || fallback?.es || fallback || "Routine").trim();
  const reviewedFallbackSpanish = String(fallback?.es || "").trim();
  const fallbackSpanish = (reviewedFallbackSpanish.toLowerCase() !== "rutina diaria" ? reviewedFallbackSpanish : "")
    || localizeRoutineContext(fallbackEnglish)
    || "Rutina diaria";
  if (value && typeof value === "object") {
    const en = String(value.en || value.es || "").trim();
    const reviewedSpanish = String(value.es || "").trim();
    const es = (reviewedSpanish
      && reviewedSpanish.toLowerCase() !== en.toLowerCase()
      && reviewedSpanish.toLowerCase() !== "rutina diaria"
      ? reviewedSpanish
      : "")
      || localizeRoutineContext(en)
      || fallbackSpanish;
    if (en || es) return { en: en || fallbackEnglish, es };
  }
  const en = String(value || "").trim();
  if (en) return { en, es: localizeRoutineContext(en) || fallbackSpanish };
  return {
    en: fallbackEnglish,
    es: fallbackSpanish
  };
};

const localizedSvgAsset = async (asset, language) => {
  if (!String(asset).toLowerCase().endsWith(".svg")) return asset;
  const response = await fetch(asset, { cache: "no-store" });
  if (!response.ok) throw new Error("The printable visual labels could not be prepared.");
  const source = await response.text();
  const svgDocument = new DOMParser().parseFromString(source, "image/svg+xml");
  if (svgDocument.querySelector("parsererror")) throw new Error("The printable visual labels could not be prepared.");
  svgDocument.querySelectorAll("text").forEach((element) => {
    const original = element.textContent.trim();
    if (/^(?:DRAFT · HUMAN REVIEW REQUIRED|BORRADOR · REVISIÓN HUMANA)$/i.test(original)) {
      element.textContent = "";
      return;
    }
    const printableText = original
      .replace(/\s*·\s*DRAFT · HUMAN REVIEW REQUIRED$/i, "")
      .replace(/\s*·\s*REVISIÓN HUMANA$/i, "")
      .trim();
    element.textContent = language === "es" && SVG_TEXT_ES[printableText]
      ? SVG_TEXT_ES[printableText]
      : printableText;
  });
  const localized = new XMLSerializer().serializeToString(svgDocument.documentElement);
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(localized)}`;
};

const renderSignIllustration = (image, candidate, word, revision) => {
  image.alt = builder.language === "es"
    ? `Ilustración revisada del signo ${word}`
    : `${word} sign illustration, ${candidate.title.toLowerCase()}`;
  image.dataset.sourceAsset = candidate.asset;
  image.hidden = true;
  image.removeAttribute("src");
  const reveal = async (asset) => {
    if (revision !== builder.renderRevision) return false;
    image.src = asset;
    if (typeof image.decode === "function") await image.decode();
    if (revision !== builder.renderRevision) return false;
    image.hidden = false;
    return true;
  };
  return localizedSvgAsset(candidate.asset, builder.language)
    .then(reveal)
    .catch(async () => {
      if (revision !== builder.renderRevision) return false;
      try {
        const ready = await reveal(candidate.asset);
        if (ready) {
          status.textContent = builder.language === "es"
            ? "La ilustración está disponible, pero no se pudieron preparar todas las etiquetas en español."
            : "The illustration is available, but its printable labels could not be prepared.";
        }
        return ready;
      } catch (_error) {
        if (revision === builder.renderRevision) {
          image.hidden = true;
          image.removeAttribute("src");
        }
        return false;
      }
    });
};

const renderContextImage = (visualPackage, copy) => {
  const contextImage = card.querySelector("[data-context-image]");
  const placeholder = card.querySelector("[data-context-placeholder]");
  const asset = visualPackage.contextual_image?.asset;
  const showPlaceholder = () => {
    contextImage.hidden = true;
    contextImage.removeAttribute("src");
    contextImage.alt = "";
    placeholder.hidden = false;
    placeholder.querySelector("strong").textContent = copy.missingContext;
  };
  if (!asset) {
    showPlaceholder();
    return false;
  }
  contextImage.hidden = true;
  placeholder.hidden = true;
  contextImage.alt = builder.language === "es"
    ? copy.context
    : visualPackage.contextual_image.alt || copy.context;
  contextImage.onload = () => { contextImage.hidden = false; placeholder.hidden = true; };
  contextImage.onerror = showPlaceholder;
  contextImage.src = asset;
  if (contextImage.complete && contextImage.naturalWidth > 0) contextImage.onload();
  return true;
};

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
const visualPackageFor = (sign) => builder.visualPackages.find((item) => item.sign_id === sign?.sign_id);
const approvedCandidateFor = (sign) => {
  const visualPackage = visualPackageFor(sign);
  const approval = builder.approvedVisual;
  if (!sign
    || !visualPackage
    || approval?.sign_id !== sign.sign_id
    || approval?.status !== "APPROVED_FOR_INTERNAL_PRINTABLE"
    || approval?.internal_printable_eligible !== true
    || !approval?.content_hash) return null;
  return [...visualPackage.candidates, ...(visualPackage.regeneration_candidates || [])].find((candidate) => (
    candidate.id === approval.candidate_id
    && candidate.asset === approval.asset
    && Boolean(candidate.content_hash)
    && candidate.content_hash === approval.content_hash
  )) || null;
};
const isEligible = (sign) => Boolean(approvedCandidateFor(sign));
const signOptionLabel = (sign) => isEligible(sign)
  ? `${sign.display_name} — Ready to create a printable`
  : `${sign.display_name} — Complete the visual review first`;

const loadApprovedVisual = () => {
  const parameters = new URLSearchParams(window.location.search);
  if (parameters.get("approved") !== "1" && parameters.get("restore") !== "1" && parameters.get("reviewed") !== "1") return null;
  const payload = readStoredPayload("kinderflowApprovedVisual");
  const workflow = readStoredPayload("kinderflowVisualWorkflow");
  const requestedRun = parameters.get("source_run");
  const requestedCandidate = parameters.get("visual");
  return payload?.status === "APPROVED_FOR_INTERNAL_PRINTABLE"
    && payload.internal_printable_eligible === true
    && payload.publication_status === "DRAFT"
    && payload.sign_id
    && payload.asset
    && payload.content_hash
    && workflow?.cv_run_id === payload.cv_run_id
    && workflow?.sign_id === payload.sign_id
    && workflow?.selected_candidate_id === payload.candidate_id
    && workflow?.visual_review_status === "APPROVED_FOR_INTERNAL_PRINTABLE"
    && workflow?.internal_printable_eligible === true
    && workflow?.publication_status === "DRAFT"
    && (!requestedRun || requestedRun === payload.cv_run_id)
    && (!requestedCandidate || requestedCandidate === payload.candidate_id)
    ? payload
    : null;
};

const loadPrintableApproval = () => {
  if (new URLSearchParams(window.location.search).get("restore") !== "1") return null;
  const payload = readStoredPayload("kinderflowPrintableApproval");
  return payload?.status === "PRINTABLE_READY"
    && payload.publication_status === "DRAFT"
    && payload.sign_id
    && payload.candidate_id
    && payload.asset
    && hasBilingualCopy(payload.routine_context)
    && hasBilingualCopy(payload.family_guidance)
    ? payload
    : null;
};

const loadPrintablePreferences = () => {
  const payload = readStoredPayload("kinderflowPrintablePreferences");
  return payload
    && payload.sign_id
    && ["en", "es"].includes(payload.language)
    && ["flashcard", "routine"].includes(payload.card_type)
    ? payload
    : null;
};

const persistPrintablePreferences = () => {
  const sign = selectedSign();
  if (!sign) return;
  builder.printablePreferences = {
    sign_id: sign.sign_id,
    language: builder.language,
    card_type: builder.cardType
  };
  sessionStorage.setItem("kinderflowPrintablePreferences", JSON.stringify(builder.printablePreferences));
};

const loadReviewedHandoff = () => {
  if (new URLSearchParams(window.location.search).get("reviewed") !== "1") return null;
  const payload = readStoredPayload("kinderflowReviewedContentPack");
  const bilingual = (value) => value?.en?.trim() && value?.es?.trim();
  if (!payload || payload.review_status !== "APPROVED" || payload.human_review?.approved !== true || !payload.sign_id || !bilingual(payload.family_guidance) || !bilingual(payload.routine_context)) return null;
  return payload;
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

const routineContextFor = (sign, candidate) => {
  const workflow = readStoredPayload("kinderflowVisualWorkflow");
  const packageRoutine = visualPackageFor(sign)?.routine;
  const fallback = sign.routine || packageRoutine;
  const requestedRoutine = builder.requestedSignId === sign.sign_id ? builder.requestedRoutine : null;
  const printableRoutine = printableApprovalMatchesApprovedVisual(sign, candidate)
    ? builder.printableApproval.routine_context
    : null;
  const approvedRoutine = builder.approvedVisual?.sign_id === sign.sign_id ? builder.approvedVisual.routine_context : null;
  const workflowRoutine = workflow?.sign_id === sign.sign_id ? workflow.routine_context : null;
  return normalizeRoutineContext(printableRoutine || approvedRoutine || workflowRoutine || requestedRoutine, fallback);
};

const resetApproval = ({ eligible = true } = {}) => {
  builder.layoutReviewed = false;
  preApprovalActions.hidden = !eligible;
  postApprovalActions.hidden = true;
  reviewButton.disabled = true;
  reviewButton.textContent = "Approve printable";
  printButton.textContent = "Print / Save as PDF";
  reviewStateText.textContent = eligible ? "Ready for approval" : "Visual approval needed";
  state.textContent = eligible ? "Ready for approval" : "Visual approval needed";
  state.className = eligible ? "status-pill status-review" : "status-pill status-fail";
};

const outputFor = (sign, candidate) => {
  builder.routineContext = routineContextFor(sign, candidate);
  const guidanceSource = printableApprovalMatches(sign, candidate)
    ? builder.printableApproval.family_guidance
    : sign.short_family_guidance;
  builder.familyGuidance = {
    en: String(guidanceSource.en).trim(),
    es: String(guidanceSource.es).trim()
  };
  return {
    routine: builder.routineContext[builder.language],
    guidance: builder.familyGuidance[builder.language]
  };
};

const printableApprovalMatchesApprovedVisual = (sign, candidate) => {
  const approval = builder.printableApproval;
  if (!sign || !candidate || !approval) return false;
  const workflow = readStoredPayload("kinderflowVisualWorkflow");
  const contentMatches = Boolean(
    approval?.content_hash
    && candidate.content_hash
    && approval.content_hash === candidate.content_hash
  );
  const visualMatches = builder.approvedVisual?.sign_id === sign.sign_id
    && builder.approvedVisual.candidate_id === candidate.id
    && builder.approvedVisual.asset === candidate.asset
    && builder.approvedVisual.content_hash === candidate.content_hash
    && builder.approvedVisual.status === "APPROVED_FOR_INTERNAL_PRINTABLE"
    && builder.approvedVisual.internal_printable_eligible === true
    && builder.approvedVisual.publication_status === "DRAFT";
  const workflowMatches = Boolean(
    workflow?.cv_run_id
    && workflow.cv_run_id === builder.approvedVisual?.cv_run_id
    && workflow.sign_id === sign.sign_id
    && workflow.selected_candidate_id === candidate.id
    && workflow.visual_review_status === "APPROVED_FOR_INTERNAL_PRINTABLE"
    && workflow.internal_printable_eligible === true
    && workflow.publication_status === "DRAFT"
  );
  const approvedCopyMatches = hasBilingualCopy(approval?.routine_context)
    && hasBilingualCopy(approval?.family_guidance);
  return Boolean(approval.sign_id === sign.sign_id
    && approval.candidate_id === candidate.id
    && approval.asset === candidate.asset
    && ["flashcard", "routine"].includes(approval.card_type)
    && ["en", "es"].includes(approval.language)
    && approvedCopyMatches
    && contentMatches
    && visualMatches
    && workflowMatches);
};

const printableApprovalMatches = (sign, candidate) => printableApprovalMatchesApprovedVisual(sign, candidate)
  && builder.printableApproval.card_type === builder.cardType
  && builder.printableApproval.language === builder.language;

const restorePrintableReady = (sign, candidate) => {
  if (!printableApprovalMatches(sign, candidate)) return false;
  builder.layoutReviewed = true;
  preApprovalActions.hidden = true;
  postApprovalActions.hidden = false;
  reviewStateText.textContent = "Printable ready";
  state.textContent = "Printable ready";
  state.className = "status-pill status-ready";
  printButton.textContent = "Print / Save as PDF";
  printButton.disabled = typeof window.print !== "function";
  status.textContent = "Printable ready. Your approved visual and printable settings have been restored.";
  return true;
};

const render = () => {
  const revision = ++builder.renderRevision;
  const sign = selectedSign();
  if (!sign) {
    resetApproval({ eligible: false });
    card.hidden = true;
    previewEmpty.hidden = false;
    previewTitle.textContent = "Sign not available";
    previewEmpty.querySelector(".card-label").textContent = "Choose another sign";
    previewEmpty.querySelector("h3").textContent = "This sign is not available in the current demo set.";
    previewEmpty.querySelector("p:not(.card-label)").textContent = "Choose an available sign, or go back to the visual options.";
    document.querySelector("#sign-source-help").textContent = builder.unsupportedRequest
      ? `${builder.unsupportedRequest} is not available in this demo.`
      : "Choose an available sign.";
    status.textContent = "Choose another sign to continue.";
    return;
  }
  const eligible = isEligible(sign);
  const visualPackage = visualPackageFor(sign);
  resetApproval({ eligible });
  card.hidden = !eligible;
  previewEmpty.hidden = eligible;

  if (!eligible) {
    previewTitle.textContent = `${sign.display_name} · Complete the visual review first`;
    previewEmpty.querySelector(".card-label").textContent = "Visual approval needed";
    previewEmpty.querySelector("h3").textContent = "Approve a sign visual before creating printable materials.";
    previewEmpty.querySelector("p:not(.card-label)").textContent = "Go back to the visual options to choose and approve an illustration.";
    document.querySelector("#sign-source-help").textContent = `${sign.display_name} needs an approved visual before printable creation.`;
    status.textContent = "Go back to the visual options, or choose another sign.";
    return;
  }

  const candidate = approvedCandidateFor(sign);
  builder.activeCandidate = candidate;
  const copy = OUTPUT_COPY[builder.language];
  const output = outputFor(sign, candidate);
  const word = builder.language === "es" ? sign.spanish_label : sign.display_name;
  card.dataset.cardType = builder.cardType;
  card.lang = builder.language;
  card.querySelector("[data-card-sign]").textContent = word;
  const secondaryWord = card.querySelector("[data-card-spanish]");
  secondaryWord.textContent = sign.spanish_label;
  secondaryWord.hidden = builder.language !== "en";
  card.querySelector('[data-card-label="routine"]').textContent = copy.routine;
  card.querySelector('[data-card-label="guidance"]').textContent = copy.guidance;
  card.querySelector("[data-card-routine]").textContent = output.routine;
  card.querySelector("[data-card-guidance]").textContent = output.guidance;
  card.querySelector("[data-card-kind]").textContent = copy.cardKinds[builder.cardType];
  card.querySelector("[data-context-caption]").textContent = copy.context;
  const movementCopy = MOVEMENT_COPY[sign.sign_id]?.[builder.language]
    || (builder.language === "es" ? "REVISAR EL MOVIMIENTO" : visualPackage.movement.presentation);
  const movementCaption = card.querySelector("[data-movement-caption]");
  const movementIcon = document.createElement("span");
  movementIcon.setAttribute("aria-hidden", "true");
  movementIcon.textContent = "↔";
  movementCaption.replaceChildren(movementIcon, ` ${movementCopy}`);
  const signIllustration = card.querySelector("[data-sign-illustration]");
  const illustrationReady = renderSignIllustration(signIllustration, candidate, word, revision);
  const hasContextImage = renderContextImage(visualPackage, copy);
  card.querySelector("[data-context-panel]").hidden = builder.cardType !== "flashcard";
  card.querySelector("[data-routine-icon]").hidden = builder.cardType !== "routine";
  card.querySelector("[data-routine-icon] span").textContent = output.routine;
  card.querySelector("[data-routine-icon]").setAttribute(
    "aria-label",
    builder.language === "es" ? `Icono de rutina: ${output.routine}` : `${output.routine} routine icon`
  );
  card.querySelector(".flashcard-visual").setAttribute(
    "aria-label",
    builder.language === "es"
      ? `Ilustración revisada del signo ${word}${builder.cardType === "flashcard" ? " con contexto de la vida cotidiana" : " con un icono de rutina"}`
      : `${word} approved sign illustration${builder.cardType === "flashcard" ? " with a supporting early-childhood context" : " with a routine icon"}`
  );
  card.setAttribute(
    "aria-label",
    builder.language === "es"
      ? `Vista previa de ${copy.cardKinds[builder.cardType].toLowerCase()} de Kinder Signs para ${word}`
      : `Kinder Signs ${builder.cardType === "flashcard" ? "flashcard" : "routine card"} preview for ${word}`
  );
  previewTitle.textContent = `${builder.cardType === "flashcard" ? "Flashcard" : "Routine Card"} · ${copy.language}`;
  document.querySelector("#sign-source-help").textContent = `${sign.display_name} uses the approved visual from the sign journey.`;
  status.textContent = builder.language === "es"
    ? `${builder.cardType === "flashcard" ? "Tarjeta didáctica" : "Tarjeta de rutina"} en español lista. ${builder.cardType === "flashcard" ? (hasContextImage ? "Imagen de contexto incluida." : `${copy.missingContext}.`) : "No se usa una imagen de contexto."}`
    : `${builder.cardType === "flashcard" ? "Flashcard" : "Routine Card"} preview ready. ${builder.cardType === "flashcard" ? (hasContextImage ? "Context image included." : `${copy.missingContext}.`) : "No contextual photo is used."}`;
  illustrationReady.then((ready) => {
    if (revision !== builder.renderRevision) return;
    if (!ready) {
      reviewButton.disabled = true;
      reviewStateText.textContent = "Visual unavailable";
      state.textContent = "Visual unavailable";
      state.className = "status-pill status-fail";
      status.textContent = builder.language === "es"
        ? "No se pudo cargar la ilustración. Vuelve a las opciones visuales e inténtalo de nuevo."
        : "The illustration could not be loaded. Return to the visual options and try again.";
      return;
    }
    reviewButton.disabled = false;
    restorePrintableReady(sign, candidate);
  });
};

const updateReturnLinks = () => {
  const workflow = readStoredPayload("kinderflowVisualWorkflow");
  const runId = builder.approvedVisual?.cv_run_id || workflow?.cv_run_id;
  const base = runId ? { restore: "1", run: runId } : {};
  const visualReturn = `create-sign.html?${new URLSearchParams({ ...base, view: "visual-options" }).toString()}`;
  document.querySelector("#back-to-visual-options").href = visualReturn;
  document.querySelector("#empty-back-to-visual-options").href = visualReturn;
  document.querySelector("#back-to-family-materials").href = `create-sign.html?${new URLSearchParams({ ...base, view: "family-materials" }).toString()}`;
  document.querySelector("#choose-another-sign").href = "create-sign.html#setup-title";
  const sign = selectedSign();
  document.querySelector("#make-available-to-nursery").href = sign
    ? `school.html?${new URLSearchParams({ sign: sign.sign_id, focus: "share" }).toString()}`
    : "school.html#assign";
};

const populateSignSelect = () => {
  const eligibleGroup = document.createElement("optgroup");
  eligibleGroup.label = "Ready for printable creation";
  const unavailableGroup = document.createElement("optgroup");
  unavailableGroup.label = "Complete visual review first";
  builder.signs.forEach((sign) => {
    const option = document.createElement("option");
    option.value = sign.id;
    option.textContent = signOptionLabel(sign);
    (isEligible(sign) ? eligibleGroup : unavailableGroup).append(option);
  });
  signSelect.replaceChildren(eligibleGroup, unavailableGroup);
  const parameters = new URLSearchParams(window.location.search);
  const requestedValue = parameters.get("sign")?.trim() || builder.printableApproval?.sign_id || "";
  builder.requestedRoutine = parameters.get("routine")?.trim() || null;
  const requested = requestedValue.toUpperCase();
  const requestedSign = requested
    ? builder.signs.find((sign) => sign.display_name.toUpperCase() === requested || sign.sign_id.toUpperCase() === requested)
    : null;
  if (requested && !requestedSign) {
    builder.unsupportedRequest = requestedValue;
    builder.selectedId = null;
    const unsupportedOption = new Option(`${requestedValue} — Not available in this demo`, "__unsupported__", true, true);
    signSelect.prepend(unsupportedOption);
    signSelect.value = "__unsupported__";
  } else {
    builder.unsupportedRequest = null;
    builder.selectedId = requestedSign?.id || builder.signs.find(isEligible)?.id || builder.signs[0].id;
    builder.requestedSignId = requestedSign?.sign_id || null;
    signSelect.value = builder.selectedId;
  }
  const selectedRecord = requestedSign || builder.signs.find((sign) => sign.id === builder.selectedId);
  const requestedLanguage = parameters.get("lang");
  const requestedType = parameters.get("type");
  if (builder.printableApproval?.sign_id === selectedRecord?.sign_id
    && ["en", "es"].includes(builder.printableApproval.language)
    && ["flashcard", "routine"].includes(builder.printableApproval.card_type)
    && (!requestedLanguage || requestedLanguage === builder.printableApproval.language)
    && (!requestedType || requestedType === builder.printableApproval.card_type)) {
    builder.language = builder.printableApproval.language;
    builder.cardType = builder.printableApproval.card_type;
    document.querySelector(`input[name="language"][value="${builder.language}"]`).checked = true;
    document.querySelector(`input[name="card_type"][value="${builder.cardType}"]`).checked = true;
  } else {
    const savedPreferences = builder.printablePreferences?.sign_id === selectedRecord?.sign_id
      ? builder.printablePreferences
      : null;
    builder.language = ["en", "es"].includes(requestedLanguage)
      ? requestedLanguage
      : savedPreferences?.language || builder.language;
    builder.cardType = ["flashcard", "routine"].includes(requestedType)
      ? requestedType
      : savedPreferences?.card_type || builder.cardType;
    document.querySelector(`input[name="language"][value="${builder.language}"]`).checked = true;
    document.querySelector(`input[name="card_type"][value="${builder.cardType}"]`).checked = true;
  }
  signSelect.disabled = builder.signs.length === 0;
  persistPrintablePreferences();
  updateReturnLinks();
};

const loadSigns = async () => {
  try {
    const [signResponse, visualResponse] = await Promise.all([
      fetch("data/signs.json", { cache: "no-store" }),
      fetch("data/visual_sign_packages.json", { cache: "no-store" })
    ]);
    if (!signResponse.ok) throw new Error("The sign library could not be loaded.");
    if (!visualResponse.ok) throw new Error("The sign visuals could not be loaded.");
    builder.signs = validateSignData(await signResponse.json());
    const visualPayload = await visualResponse.json();
    if (!Array.isArray(visualPayload.signs)) throw new Error("The sign visuals could not be read.");
    builder.visualPackages = visualPayload.signs;
    builder.approvedVisual = loadApprovedVisual();
    builder.printableApproval = loadPrintableApproval();
    builder.printablePreferences = loadPrintablePreferences();
    if (builder.printableApproval) {
      const approvalSign = builder.signs.find((sign) => sign.sign_id === builder.printableApproval.sign_id);
      const approvalCandidate = approvedCandidateFor(approvalSign);
      if (!printableApprovalMatchesApprovedVisual(approvalSign, approvalCandidate)) {
        builder.printableApproval = null;
        sessionStorage.removeItem("kinderflowPrintableApproval");
      }
    }
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

signSelect.addEventListener("change", () => {
  builder.unsupportedRequest = signSelect.value === "__unsupported__" ? builder.unsupportedRequest : null;
  builder.selectedId = signSelect.value === "__unsupported__" ? null : signSelect.value;
  builder.requestedSignId = null;
  builder.printableApproval = null;
  sessionStorage.removeItem("kinderflowPrintableApproval");
  persistPrintablePreferences();
  render();
});
document.querySelectorAll('input[name="language"]').forEach((input) => input.addEventListener("change", () => {
  builder.language = input.value;
  builder.printableApproval = null;
  sessionStorage.removeItem("kinderflowPrintableApproval");
  persistPrintablePreferences();
  render();
}));
document.querySelectorAll('input[name="card_type"]').forEach((input) => input.addEventListener("change", () => {
  builder.cardType = input.value;
  builder.printableApproval = null;
  sessionStorage.removeItem("kinderflowPrintableApproval");
  persistPrintablePreferences();
  render();
}));

reviewButton.addEventListener("click", () => {
  const sign = selectedSign();
  if (reviewButton.disabled || !isEligible(sign)) return;
  builder.layoutReviewed = true;
  preApprovalActions.hidden = true;
  postApprovalActions.hidden = false;
  state.className = "status-pill status-ready";
  reviewStateText.textContent = "Printable ready";
  state.textContent = "Printable ready";
  reviewButton.textContent = "Printable approved";
  printButton.textContent = "Print / Save as PDF";
  printButton.disabled = typeof window.print !== "function";
  builder.printableApproval = {
    sign_id: sign.sign_id,
    sign_label_en: sign.display_name,
    sign_label_es: sign.spanish_label,
    candidate_id: builder.activeCandidate.id,
    approved_visual: builder.activeCandidate.id,
    asset: builder.activeCandidate.asset,
    content_hash: builder.activeCandidate.content_hash || builder.approvedVisual?.content_hash || null,
    card_type: builder.cardType,
    language: builder.language,
    routine_context: builder.routineContext,
    family_guidance: builder.familyGuidance,
    illustrative_video_available: ILLUSTRATIVE_VIDEO_SIGNS.has(sign.sign_id),
    selected_materials: [
      ...(ILLUSTRATIVE_VIDEO_SIGNS.has(sign.sign_id) ? ["video"] : []),
      builder.cardType === "routine" ? "routine-card" : "flashcard"
    ],
    group: "Group 1–2",
    audience_type: "group",
    child_id: "",
    assignment_id: null,
    status: "PRINTABLE_READY",
    publication_status: "DRAFT",
    approved_at: new Date().toISOString()
  };
  sessionStorage.setItem("kinderflowPrintableApproval", JSON.stringify(builder.printableApproval));
  persistPrintablePreferences();
  status.textContent = printButton.disabled
    ? "The printable is approved, but browser printing is not available."
    : "Printable ready. You can now print it or save it as a PDF.";
});

printButton.addEventListener("click", () => {
  if (!builder.layoutReviewed || printButton.disabled) return;
  const sign = selectedSign();
  const params = new URLSearchParams({
    sign: sign.sign_id,
    type: builder.cardType,
    lang: builder.language,
    asset: builder.activeCandidate.id,
    routine: builder.routineContext.en
  });
  status.textContent = "Opening the dedicated A5 print proof.";
  window.location.assign(`print-card.html?${params.toString()}`);
});

document.querySelector("#create-another").addEventListener("click", () => {
  builder.printableApproval = null;
  sessionStorage.removeItem("kinderflowPrintableApproval");
  persistPrintablePreferences();
  render();
  status.textContent = "Approved sign visual kept. Choose another format or language, then review the new printable.";
  document.querySelector('input[name="card_type"]:checked').focus();
});

loadSigns();
