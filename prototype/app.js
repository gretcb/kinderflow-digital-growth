"use strict";

const FALLBACK_SIGN_DATA = {
  sign: "More",
  routine: ["Snack time", "Playtime"],
  age_range: "0-3",
  format: ["video", "routine card", "family guidance"],
  school_assignment: {
    classroom_group: "Toddlers",
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
const assignmentConfirmation = document.querySelector("#assignment-confirmation");
const childSelect = document.querySelector("#child-select");

const bindAssignmentMode = (form, radioName, childSelector) => {
  const updateChildSelector = () => {
    const selectedMode = form.querySelector(`input[name="${radioName}"]:checked`).value;
    childSelector.disabled = selectedMode !== "child";
  };

  form.querySelectorAll(`input[name="${radioName}"]`).forEach((radio) => {
    radio.addEventListener("change", updateChildSelector);
  });
  updateChildSelector();
};

if (selectButton && assignmentForm) {
  bindAssignmentMode(assignmentForm, "assignment_mode", childSelect);

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
    const routines = signData.routine.join(" or ").toLowerCase();
    const assignmentMode = new FormData(assignmentForm).get("assignment_mode");
    const isGroupAssignment = assignmentMode === "group";

    familyMessage = [
      `This week at school, children are using the Kinder Sign “${signData.sign}”.`,
      `At home, use it during ${routines} when your child wants more of something.`,
      "Say the word while showing the sign. Repeat it naturally in the same routine.",
      "This is routine guidance, not clinical advice. It does not promise faster development. Do not force repetition."
    ].join("\n\n");

    familyMessageElement.textContent = familyMessage;
    assignmentStatus.textContent = isGroupAssignment ? "Assigned to group" : `Assigned to ${childSelect.value}`;
    assignmentConfirmation.textContent = isGroupAssignment
      ? "MORE assigned to Group A — 1–2 years. Family card prepared for all active children. Premium materials prepared only where active."
      : `MORE assigned to ${childSelect.value}. Family card prepared for the child’s family. Premium materials prepared based on active child/family access.`;
    actionStatus.textContent = "Approved family guidance ready to share.";
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
      actionStatus.textContent = "Family guidance copied.";
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
const adminControlStatus = document.querySelector("#admin-control-status");
const adminChildSelect = document.querySelector("#admin-child-select");

if (adminAssignmentForm) {
  bindAssignmentMode(adminAssignmentForm, "admin_assignment_mode", adminChildSelect);

  document.querySelectorAll("[data-admin-action]").forEach((button) => {
    button.addEventListener("click", () => {
      adminControlStatus.textContent =
        `${button.dataset.adminAction} is a visual prototype control. No school records were changed.`;
    });
  });

  adminAssignmentForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const assignmentMode = new FormData(adminAssignmentForm).get("admin_assignment_mode");
    const isGroupAssignment = assignmentMode === "group";
    adminAssignmentStatus.classList.remove("is-warning");
    adminAssignmentStatus.textContent = isGroupAssignment
      ? "MORE assigned to Group A — 1–2 years. Family card prepared for all active children. Premium materials prepared only where active."
      : `MORE assigned to ${adminChildSelect.value}. Family card prepared for the child’s family. Premium materials prepared based on active child/family access.`;
  });
}

loadSignData();
