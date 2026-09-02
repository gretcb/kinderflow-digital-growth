"use strict";

const candidateList = document.querySelector("#character-candidate-list");
const saveCandidateButton = document.querySelector("#save-character-candidate");
const characterReviewStatus = document.querySelector("#character-review-status");
let characterCandidates = [];
let selectedCandidate = null;

const componentName = (path) => path?.split("/").at(-1)?.replace(/\.svg$/i, "") || "—";

const renderCharacterSummary = () => {
  const candidate = characterCandidates.find((item) => item.candidate_id === selectedCandidate);
  document.querySelector("#character-selection-title").textContent = candidate ? candidate.candidate_id.replaceAll("_", " ") : "No candidate selected";
  document.querySelector("#character-face").textContent = componentName(candidate?.face);
  document.querySelector("#character-hair").textContent = componentName(candidate?.hair);
  document.querySelector("#character-body").textContent = componentName(candidate?.body);
  document.querySelector("#character-base").textContent = componentName(candidate?.base);
  document.querySelector("#character-accessories").textContent = candidate?.accessories || "—";
  saveCandidateButton.disabled = !candidate;
};

const renderCharacterCandidates = () => {
  candidateList.replaceChildren(...characterCandidates.map((candidate, index) => {
    const label = document.createElement("label");
    label.className = "character-candidate";
    const input = document.createElement("input");
    input.type = "radio";
    input.name = "character_candidate";
    input.value = candidate.candidate_id;
    input.checked = index === 0;
    const copy = document.createElement("span");
    const title = document.createElement("strong");
    const parts = document.createElement("small");
    const reason = document.createElement("em");
    title.textContent = candidate.candidate_id.replaceAll("_", " ");
    parts.textContent = `${componentName(candidate.face)} face · ${componentName(candidate.hair)} hair · ${componentName(candidate.body)}`;
    reason.textContent = candidate.why_shortlisted;
    copy.append(title, parts, reason);
    label.append(input, copy);
    return label;
  }));
  selectedCandidate = characterCandidates[0]?.candidate_id || null;
  renderCharacterSummary();
};

candidateList?.addEventListener("change", (event) => {
  if (event.target.name !== "character_candidate") return;
  selectedCandidate = event.target.value;
  renderCharacterSummary();
  characterReviewStatus.textContent = "Candidate selected for comparison. No final character or licence decision has been recorded.";
});

saveCandidateButton?.addEventListener("click", () => {
  if (!selectedCandidate) return;
  sessionStorage.setItem("kinderflowCharacterCandidate", selectedCandidate);
  characterReviewStatus.textContent = "Candidate saved in this browser session for founder review. This is not final artwork approval.";
});

const loadCharacterCandidates = async () => {
  if (!candidateList) return;
  try {
    const response = await fetch("/api/visual-assets/open-peeps", { cache: "no-store" });
    if (!response.ok) throw new Error("Candidate metadata is unavailable.");
    const payload = await response.json();
    if (payload.licence_status !== "LICENCE_VERIFICATION_NEEDED" || !Array.isArray(payload.candidates)) throw new Error("Candidate metadata is invalid.");
    characterCandidates = payload.candidates;
    renderCharacterCandidates();
  } catch (error) {
    const message = document.createElement("p");
    message.textContent = `${error.message} The Flashcard Studio will continue to use its labelled placeholder.`;
    candidateList.replaceChildren(message);
    characterReviewStatus.textContent = "Character candidates unavailable; final visual remains blocked.";
  }
};

loadCharacterCandidates();
