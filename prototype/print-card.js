"use strict";

const COPY = {
  en: { routine: "Routine", guidance: "How to use it", context: "Everyday context" },
  es: { routine: "Rutina", guidance: "Cómo usarlo", context: "Contexto cotidiano" }
};

const status = document.querySelector("#print-card-status");
const card = document.querySelector("#a5-print-card");
const printButton = document.querySelector("#open-print-dialog");
const errorPanel = document.querySelector("#print-card-error");

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

const waitForImages = async () => {
  const images = [...card.querySelectorAll("img")];
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
  const signId = params.get("sign")?.trim().toLowerCase();
  const cardType = params.get("type");
  const language = params.get("lang");
  const assetId = params.get("asset");
  if (!signId || !["flashcard", "routine"].includes(cardType) || !["en", "es"].includes(language) || !assetId) {
    fail("The print request is incomplete. Return to the printable builder and try again.");
    return;
  }
  const approval = loadApproval();
  if (!approval || approval.status !== "PRINTABLE_READY" || approval.publication_status !== "DRAFT" || approval.sign_id !== signId || approval.candidate_id !== assetId || approval.card_type !== cardType || approval.language !== language) {
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
    if (!sign || !signPackage) throw new Error("This sign does not have a reviewed visual package.");
    const candidates = [...signPackage.candidates, ...(signPackage.regeneration_candidates || [])];
    const candidate = candidates.find((item) => item.id === assetId && item.asset === approval.asset);
    if (!candidate) throw new Error("The approved visual cannot be found. Return to visual review and approve an available candidate.");
    if (cardType === "flashcard" && !signPackage.contextual_image?.asset) throw new Error("A reviewed contextual image is required for this Flashcard. Choose Routine Card or return to visual review.");

    const copy = COPY[language];
    const word = language === "es" ? sign.spanish_label : sign.display_name;
    const routine = signPackage.routine[language];
    const guidance = signPackage.routine_guidance[language];
    const signAlt = `${word} sign illustration for human-reviewed internal printing`;
    card.dataset.cardType = cardType;
    card.querySelector("[data-print-kind]").textContent = cardType === "flashcard" ? "FLASHCARD" : "ROUTINE CARD";
    card.querySelector("[data-print-word]").textContent = word;
    card.querySelector("[data-context-caption]").textContent = copy.context;
    card.querySelector("[data-routine-label]").textContent = copy.routine;
    card.querySelector("[data-guidance-label]").textContent = copy.guidance;
    card.querySelector("[data-print-routine-name]").textContent = routine;
    card.querySelector("[data-print-guidance]").textContent = guidance;
    card.querySelector("[data-movement-caption]").textContent = signPackage.movement.presentation;
    const flashcardArea = card.querySelector("[data-print-flashcard]");
    const routineArea = card.querySelector("[data-print-routine]");
    if (cardType === "flashcard") {
      flashcardArea.hidden = false;
      routineArea.remove();
      const contextImage = card.querySelector("[data-print-context]");
      contextImage.src = signPackage.contextual_image.asset;
      contextImage.alt = signPackage.contextual_image.alt;
      const signImage = card.querySelector("[data-print-sign]");
      signImage.src = candidate.asset;
      signImage.alt = signAlt;
    } else {
      routineArea.hidden = false;
      flashcardArea.remove();
      const signImage = card.querySelector("[data-print-routine-sign]");
      signImage.src = candidate.asset;
      signImage.alt = signAlt;
    }
    card.setAttribute("aria-label", `Kinder Signs A5 ${cardType === "flashcard" ? "Flashcard" : "Routine Card"} for ${word}`);
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
