"use strict";

const COPY = {
  en: {
    routine: "Routine",
    guidance: "How to use it",
    context: "Everyday context",
    missingContext: "Context image not prepared yet",
    footer: "Printable proof",
    cardKinds: { flashcard: "FLASHCARD", routine: "ROUTINE CARD" }
  },
  es: {
    routine: "Rutina",
    guidance: "Cómo usarlo",
    context: "Contexto cotidiano",
    missingContext: "Imagen de contexto aún no preparada",
    footer: "Prueba imprimible",
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

const status = document.querySelector("#print-card-status");
const card = document.querySelector("#a5-print-card");
const printButton = document.querySelector("#open-print-dialog");
const errorPanel = document.querySelector("#print-card-error");
const returnLink = document.querySelector("#return-to-builder");
const visualReturnLink = document.querySelector("#return-to-visual-review");

const fail = (message) => {
  card.hidden = true;
  errorPanel.hidden = false;
  document.querySelector("#print-card-error-message").textContent = message;
  status.textContent = "Printable unavailable.";
};

const loadApproval = () => {
  try {
    return JSON.parse(sessionStorage.getItem("kinderflowPrintableApproval") || "null");
  } catch (_error) {
    return null;
  }
};

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

const prepareRecoveryLinks = (params) => {
  const approval = loadApproval();
  const approvedVisual = readStoredPayload("kinderflowApprovedVisual");
  const workflow = readStoredPayload("kinderflowVisualWorkflow");
  const returnState = {
    restore: "1",
    approved: "1"
  };
  const values = {
    sign: params.get("sign") || approval?.sign_id,
    asset: params.get("asset") || approval?.candidate_id,
    visual: params.get("asset") || approval?.candidate_id,
    type: params.get("type") || approval?.card_type,
    lang: params.get("lang") || approval?.language,
    routine: params.get("routine") || approval?.routine_context?.en
  };
  Object.entries(values).forEach(([key, value]) => {
    if (value) returnState[key] = value;
  });
  returnLink.href = `flashcards.html?${new URLSearchParams(returnState).toString()}`;
  const runId = approvedVisual?.cv_run_id || workflow?.cv_run_id;
  visualReturnLink.href = runId
    ? `create-sign.html?${new URLSearchParams({ restore: "1", view: "visual-options", run: runId }).toString()}`
    : "create-sign.html";
};

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

const showContextPlaceholder = (copy) => {
  const contextImage = card.querySelector("[data-print-context]");
  const placeholder = card.querySelector("[data-print-context-placeholder]");
  contextImage.hidden = true;
  contextImage.removeAttribute("src");
  contextImage.alt = "";
  placeholder.hidden = false;
  placeholder.textContent = copy.missingContext;
};

const prepareContextImage = (context, copy, language) => new Promise((resolve) => {
  const contextImage = card.querySelector("[data-print-context]");
  const placeholder = card.querySelector("[data-print-context-placeholder]");
  if (!context?.asset) {
    showContextPlaceholder(copy);
    resolve(false);
    return;
  }
  contextImage.hidden = true;
  placeholder.hidden = true;
  contextImage.alt = language === "es" ? copy.context : context.alt || copy.context;
  contextImage.onload = () => {
    contextImage.hidden = false;
    placeholder.hidden = true;
    resolve(true);
  };
  contextImage.onerror = () => {
    showContextPlaceholder(copy);
    resolve(false);
  };
  contextImage.src = context.asset;
  if (contextImage.complete && contextImage.naturalWidth > 0) contextImage.onload();
});

const waitForImages = async () => {
  const images = [...card.querySelectorAll("img[src]:not([hidden])")];
  await Promise.all(images.map((image) => {
    if (image.complete && image.naturalWidth > 0) return image.decode?.().catch(() => undefined);
    return new Promise((resolve, reject) => {
      image.addEventListener("load", resolve, { once: true });
      image.addEventListener("error", reject, { once: true });
    });
  }));
  if (document.fonts?.ready) await document.fonts.ready;
};

const prepare = async () => {
  const params = new URLSearchParams(window.location.search);
  prepareRecoveryLinks(params);
  const signId = params.get("sign")?.trim().toLowerCase();
  const cardType = params.get("type");
  const language = params.get("lang");
  const assetId = params.get("asset");
  const requestedRoutine = params.get("routine")?.trim() || null;
  if (!signId || !["flashcard", "routine"].includes(cardType) || !["en", "es"].includes(language) || !assetId) {
    fail("The print request is incomplete. Return to the printable builder and try again.");
    return;
  }
  const approval = loadApproval();
  const approvedVisual = readStoredPayload("kinderflowApprovedVisual");
  const workflow = readStoredPayload("kinderflowVisualWorkflow");
  if (!approval
    || approval.status !== "PRINTABLE_READY"
    || approval.publication_status !== "DRAFT"
    || approval.sign_id !== signId
    || approval.candidate_id !== assetId
    || approval.card_type !== cardType
    || approval.language !== language
    || !approval.content_hash
    || !hasBilingualCopy(approval.routine_context)
    || !hasBilingualCopy(approval.family_guidance)
    || approvedVisual?.sign_id !== signId
    || approvedVisual?.candidate_id !== assetId
    || approvedVisual?.asset !== approval.asset
    || !approvedVisual?.content_hash
    || approvedVisual?.content_hash !== approval.content_hash
    || approvedVisual?.status !== "APPROVED_FOR_INTERNAL_PRINTABLE"
    || approvedVisual?.internal_printable_eligible !== true
    || approvedVisual?.publication_status !== "DRAFT"
    || !approvedVisual?.cv_run_id
    || workflow?.cv_run_id !== approvedVisual?.cv_run_id
    || workflow?.sign_id !== signId
    || workflow?.selected_candidate_id !== assetId
    || workflow?.visual_review_status !== "APPROVED_FOR_INTERNAL_PRINTABLE"
    || workflow?.internal_printable_eligible !== true
    || workflow?.publication_status !== "DRAFT") {
    fail("Approve this exact card in the printable builder before opening the A5 print proof.");
    return;
  }
  try {
    const [signResponse, packageResponse] = await Promise.all([
      fetch("data/signs.json", { cache: "no-store" }),
      fetch("data/visual_sign_packages.json", { cache: "no-store" })
    ]);
    if (!signResponse.ok || !packageResponse.ok) throw new Error("The local printable data is unavailable.");
    const signs = (await signResponse.json()).signs;
    const packages = (await packageResponse.json()).signs;
    const sign = signs.find((item) => item.sign_id === signId);
    const signPackage = packages.find((item) => item.sign_id === signId);
    if (!sign || !signPackage) throw new Error("This sign does not have a reviewed sign visual.");
    const candidates = [...signPackage.candidates, ...(signPackage.regeneration_candidates || [])];
    const candidate = candidates.find((item) => item.id === assetId && item.asset === approval.asset);
    if (!candidate) throw new Error("The approved sign visual cannot be found. Return to visual review and approve an available visual option.");
    if (!approval.content_hash || !candidate.content_hash || approval.content_hash !== candidate.content_hash) {
      throw new Error("The approved sign visual has changed. Return to visual review and approve the current visual option.");
    }

    const copy = COPY[language];
    const word = language === "es" ? sign.spanish_label : sign.display_name;
    const routineContext = normalizeRoutineContext(approval.routine_context || requestedRoutine, signPackage.routine || sign.routine);
    const routine = routineContext[language];
    const guidance = String(approval.family_guidance[language]).trim();
    const signAlt = language === "es"
      ? `Ilustración revisada del signo ${word}`
      : `${word} sign illustration in a human-reviewed printable proof`;
    const returnState = {
      sign: signId,
      asset: assetId,
      visual: assetId,
      approved: "1",
      restore: "1",
      type: cardType,
      lang: language,
      routine: routineContext.en
    };
    returnLink.href = `flashcards.html?${new URLSearchParams(returnState).toString()}`;
    card.dataset.cardType = cardType;
    card.lang = language;
    card.querySelector("[data-print-kind]").textContent = copy.cardKinds[cardType];
    card.querySelector("[data-print-word]").textContent = word;
    const secondaryWord = card.querySelector("[data-print-spanish]");
    secondaryWord.textContent = sign.spanish_label;
    secondaryWord.hidden = language === "es";
    card.querySelector("[data-context-caption]").textContent = copy.context;
    card.querySelector("[data-routine-label]").textContent = copy.routine;
    card.querySelector("[data-guidance-label]").textContent = copy.guidance;
    card.querySelector("[data-print-routine-name]").textContent = routine;
    card.querySelector("[data-print-guidance]").textContent = guidance;
    card.querySelector("[data-movement-caption]").textContent = MOVEMENT_COPY[signId]?.[language]
      || (language === "es" ? "REVISAR EL MOVIMIENTO" : signPackage.movement.presentation);
    card.querySelector("[data-print-footer]").textContent = copy.footer;
    card.querySelector("[data-routine-icon-title]").textContent = language === "es"
      ? `Rutina: ${routine}`
      : `${routine} routine`;
    const localizedAsset = await localizedSvgAsset(candidate.asset, language);
    const flashcardArea = card.querySelector("[data-print-flashcard]");
    const routineArea = card.querySelector("[data-print-routine]");
    if (cardType === "flashcard") {
      flashcardArea.hidden = false;
      routineArea.remove();
      await prepareContextImage(signPackage.contextual_image, copy, language);
      const signImage = card.querySelector("[data-print-sign]");
      signImage.src = localizedAsset;
      signImage.alt = signAlt;
    } else {
      routineArea.hidden = false;
      flashcardArea.remove();
      const signImage = card.querySelector("[data-print-routine-sign]");
      signImage.src = localizedAsset;
      signImage.alt = signAlt;
    }
    card.setAttribute(
      "aria-label",
      language === "es"
        ? `${copy.cardKinds[cardType]} A5 de Kinder Signs para ${word}`
        : `Kinder Signs A5 ${cardType === "flashcard" ? "Flashcard" : "Routine Card"} for ${word}`
    );
    card.hidden = false;
    await waitForImages();
    printButton.disabled = false;
    status.textContent = "A5 proof ready. Check the layout, then print or save as PDF.";
  } catch (error) {
    fail(error.message);
  }
};

printButton.addEventListener("click", async () => {
  printButton.disabled = true;
  status.textContent = "Checking images before opening the print dialog…";
  try {
    await waitForImages();
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    status.textContent = "Print dialog opened. Choose Save as PDF if needed.";
    window.print();
  } catch (_error) {
    status.textContent = "An image did not load. Return to the printable builder and try again.";
  } finally {
    printButton.disabled = false;
  }
});

prepare();
