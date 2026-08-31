"use strict";

const FALLBACK_SIGN_DATA = {
  sign: "More",
  routine: ["Snack time", "Playtime"],
  age_range: "0-3",
  format: ["video", "routine card", "family guidance"],
  school_assignment: {
    classroom_group: "Toddlers",
    child_profile: "Example child profile",
    tutors_included: 2,
    delivery: "existing school-family channel"
  },
  family_access: {
    included: "2 main tutors included",
    extra_caregiver: "Optional paid add-on",
    examples: ["Grandparent", "Nanny", "Second home"]
  },
  add_ons: [
    "printed flashcards",
    "original mini stories",
    "original short songs",
    "routine packs"
  ],
  boundaries: [
    "No child video required",
    "Family guidance, not clinical advice",
    "Internal AI workflow is not managed by the school"
  ]
};

let signData = FALLBACK_SIGN_DATA;
let familyMessage = "";

const setText = (selector, value) => {
  document.querySelectorAll(selector).forEach((element) => {
    element.textContent = value;
  });
};

const renderSignData = (data) => {
  setText("[data-sign-name]", data.sign);
  setText("[data-routine]", data.routine.join(" / "));
  setText("[data-age-range]", data.age_range);
  setText("[data-format]", data.format.map((item) => item.charAt(0).toUpperCase() + item.slice(1)).join(" + "));
  setText("[data-classroom]", data.school_assignment.classroom_group);
  setText("[data-child-profile]", data.school_assignment.child_profile);
  setText("[data-tutors]", String(data.school_assignment.tutors_included));
  setText("[data-delivery]", data.school_assignment.delivery);
};

const loadSignData = async () => {
  try {
    const response = await fetch("data/approved_sign_more.json");
    if (!response.ok) {
      throw new Error(`Local data request failed with status ${response.status}`);
    }
    signData = await response.json();
  } catch (_error) {
    // Browsers commonly block fetch for file:// pages. The embedded equivalent keeps that mode usable.
    signData = FALLBACK_SIGN_DATA;
  }
  renderSignData(signData);
};

const selectButton = document.querySelector("#select-sign");
const selectionStatus = document.querySelector("#selection-status");
const assignmentStatus = document.querySelector("#assignment-status");
const assignmentForm = document.querySelector("#assignment-form");
const familyMessageElement = document.querySelector("#family-message");
const messagePreview = document.querySelector("#message-preview");
const actionStatus = document.querySelector("#action-status");

if (selectButton && assignmentForm) {
  selectButton.addEventListener("click", () => {
    selectButton.textContent = "Weekly sign selected";
    selectButton.setAttribute("aria-pressed", "true");
    selectionStatus.textContent = "Selected";
    selectionStatus.classList.add("selected");
    assignmentStatus.textContent = `${signData.sign} selected`;
    document.querySelector("#assignment").scrollIntoView({ behavior: "smooth", block: "start" });
  });

  assignmentForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const target = new FormData(assignmentForm).get("assignment_type");
    const routines = signData.routine.join(" or ").toLowerCase();

    familyMessage = [
      `This week’s Kinder Sign is “${signData.sign}”.`,
      `Use it during ${routines} when your child wants more of something.`,
      "Say the word while showing the sign, and repeat naturally in the routine.",
      "The same sign is being used at school this week, helping provide a consistent cue.",
      "This is family guidance, not clinical advice. Do not force repetition."
    ].join("\n\n");

    familyMessageElement.textContent = familyMessage;
    assignmentStatus.textContent = `Assigned to ${target.toLowerCase()}`;
    actionStatus.textContent = "Family output generated locally.";
    messagePreview.focus();
  });
}

const copyText = async (text) => {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.setAttribute("readonly", "");
  textArea.style.position = "fixed";
  textArea.style.opacity = "0";
  document.body.appendChild(textArea);
  textArea.select();
  document.execCommand("copy");
  textArea.remove();
};

const copyMessageButton = document.querySelector("#copy-message");
const exportPdfButton = document.querySelector("#export-pdf");
const createLinkButton = document.querySelector("#create-link");

if (copyMessageButton) {
  copyMessageButton.addEventListener("click", async () => {
    const text = familyMessage || familyMessageElement.textContent.trim();
    try {
      await copyText(text);
      actionStatus.textContent = "Family message copied.";
    } catch (_error) {
      actionStatus.textContent = "Copy is unavailable in this browser. The message remains ready to select.";
    }
  });
}

if (exportPdfButton) {
  exportPdfButton.addEventListener("click", () => {
    actionStatus.textContent = "Opening the browser print dialog. Choose Save as PDF to export this prototype card.";
    window.print();
  });
}

if (createLinkButton) {
  createLinkButton.addEventListener("click", () => {
    actionStatus.textContent = "Prototype share link prepared. Nothing was published or sent.";
  });
}

const routineButton = document.querySelector("#open-routine");
const routineDetail = document.querySelector("#routine-detail");

if (routineButton) {
  routineButton.addEventListener("click", () => {
    const isOpen = routineButton.getAttribute("aria-expanded") === "true";
    routineButton.setAttribute("aria-expanded", String(!isOpen));
    routineButton.textContent = isOpen ? "Open routine card" : "Close routine card";
    routineDetail.hidden = isOpen;
  });
}

const adminAssignmentForm = document.querySelector("#admin-assignment-form");
const adminAssignmentStatus = document.querySelector("#admin-assignment-status");

if (adminAssignmentForm) {
  adminAssignmentForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const selectedGroups = adminAssignmentForm.querySelectorAll('input[name="school_group"]:checked');

    if (selectedGroups.length === 0) {
      adminAssignmentStatus.textContent = "Select at least one school group before assigning the weekly sign.";
      adminAssignmentStatus.classList.add("is-warning");
      return;
    }

    adminAssignmentStatus.classList.remove("is-warning");
    adminAssignmentStatus.textContent =
      "Assigned to selected school groups. Family card ready for the school-family channel.";
  });
}

loadSignData();
