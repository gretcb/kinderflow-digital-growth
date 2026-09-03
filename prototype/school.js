"use strict";

const SCHOOL_CONTENT = {
  more: { en: "MORE", es: "MÁS", materials: ["video", "flashcard", "routine-card", "story"] },
  help: { en: "HELP", es: "AYUDA", materials: ["video", "flashcard", "routine-card"] },
  eat: { en: "EAT", es: "COMER", materials: ["video", "flashcard", "routine-card"] },
  sleep: { en: "SLEEP", es: "DORMIR", materials: ["video", "flashcard", "routine-card"] },
  milk: { en: "MILK", es: "LECHE", materials: ["video", "flashcard", "routine-card"] },
  water: { en: "WATER", es: "AGUA", materials: ["video", "flashcard", "routine-card"] }
};

const SCHOOL_PLAN = new Set(["video", "flashcard", "routine-card", "story"]);
const MATERIAL_LABELS = {
  video: "Video",
  flashcard: "Flashcard",
  "routine-card": "Routine Card",
  story: "Story"
};
const GROUPS = {
  "Group 0–1": { short: "Babies", label: "Babies · 0–1", children: ["Child A", "Child B"] },
  "Group 1–2": { short: "Toddlers", label: "Toddlers · 1–2", children: ["Child C", "Child D"] },
  "Group 2–3": { short: "Preschool", label: "Preschool · 2–3", children: ["Child E", "Child F"] }
};
const MATERIAL_ORDER = Object.keys(MATERIAL_LABELS);
const GENERATED_ASSIGNMENT_ID = /^assignment-[1-9]\d{0,8}$/;
const normaliseMaterials = (materials) => [...new Set(materials || [])]
  .filter((material) => MATERIAL_ORDER.includes(material))
  .sort((left, right) => MATERIAL_ORDER.indexOf(left) - MATERIAL_ORDER.indexOf(right));

const DEFAULT_ASSIGNMENTS = [{
  id: "seed-more-babies",
  signId: "more",
  groupId: "Group 0–1",
  audienceType: "group",
  childId: "",
  materials: ["video", "flashcard"]
}];
const DEFAULT_ASSIGNMENT_IDS = new Set(DEFAULT_ASSIGNMENTS.map((assignment) => assignment.id));
const assignmentIdIsSafe = (id) => typeof id === "string"
  && (DEFAULT_ASSIGNMENT_IDS.has(id) || GENERATED_ASSIGNMENT_ID.test(id));

const storageAvailable = typeof sessionStorage !== "undefined";
const preferredScrollBehavior = (
  typeof window !== "undefined"
  && window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches
) ? "auto" : "smooth";
const loadAssignments = () => {
  if (!storageAvailable) return DEFAULT_ASSIGNMENTS.map((assignment) => ({ ...assignment, materials: [...assignment.materials] }));
  try {
    const saved = JSON.parse(sessionStorage.getItem("kinderflowSchoolAssignments") || "null");
    if (!Array.isArray(saved)) return DEFAULT_ASSIGNMENTS.map((assignment) => ({ ...assignment, materials: [...assignment.materials] }));
    const seenIds = new Set();
    return saved.flatMap((assignment) => {
      const materials = normaliseMaterials(assignment?.materials)
        .filter((material) => SCHOOL_CONTENT[assignment?.signId]?.materials.includes(material));
      const group = GROUPS[assignment?.groupId];
      const validAudience = ["group", "child"].includes(assignment?.audienceType);
      const validChild = assignment?.audienceType !== "child" || group?.children.includes(assignment?.childId);
      const validId = assignmentIdIsSafe(assignment?.id);
      if (!validId
        || seenIds.has(assignment.id)
        || !SCHOOL_CONTENT[assignment?.signId]
        || !group
        || !validAudience
        || !validChild
        || !materials.length) return [];
      seenIds.add(assignment.id);
      return [{ ...assignment, childId: assignment.audienceType === "child" ? assignment.childId : "", materials }];
    });
  } catch (_error) {
    return DEFAULT_ASSIGNMENTS.map((assignment) => ({ ...assignment, materials: [...assignment.materials] }));
  }
};

let assignments = loadAssignments();
let editingAssignmentId = null;
let duplicateAssignmentId = null;
let assignmentSequence = Math.max(
  assignments.length,
  ...assignments.map((assignment) => Number(String(assignment.id).match(/^assignment-(\d+)$/)?.[1] || 0))
);
const nextAssignmentId = () => {
  do {
    assignmentSequence = assignmentSequence >= 999999999 ? 1 : assignmentSequence + 1;
  } while (assignments.some((assignment) => assignment.id === `assignment-${assignmentSequence}`));
  return `assignment-${assignmentSequence}`;
};

const assignmentForm = document.querySelector("#school-assignment-form");
const signSelect = document.querySelector("#assignment-sign");
const groupSelect = document.querySelector("#assignment-group");
const materialChoices = document.querySelector("#assignment-materials");
const childPanel = document.querySelector("#assignment-child-panel");
const childSelect = document.querySelector("#assignment-child");
const assignmentStatus = document.querySelector("#school-assignment-status");
const assignmentSummary = document.querySelector("#assignment-summary");
const assignmentMaterialSummary = document.querySelector("#assignment-material-summary");
const assignmentValidation = document.querySelector("#assignment-validation");
const assignmentSubmit = document.querySelector("#assignment-submit");
const assignmentResult = document.querySelector(".assignment-result");
const duplicatePanel = document.querySelector("#duplicate-assignment");
const assignAnother = document.querySelector("#assign-another");
const cancelEdit = document.querySelector("#cancel-assignment-edit");
const activeList = document.querySelector("#active-sign-list");

const contentFor = (signId) => SCHOOL_CONTENT[signId] || null;
const availableMaterialsFor = (signId) => (contentFor(signId)?.materials || []).filter((material) => SCHOOL_PLAN.has(material));
const selectedMaterials = () => [...materialChoices.querySelectorAll('input[name="materials"]:checked')].map((input) => input.value);
const selectedAudience = () => document.querySelector('input[name="audience"]:checked')?.value || "group";

const assignmentKey = (assignment) => JSON.stringify([
  assignment.signId,
  assignment.groupId,
  assignment.audienceType === "child" ? `child:${assignment.childId}` : "group",
  normaliseMaterials(assignment.materials)
]);

const findExactDuplicate = (candidate, ignoreId = null) => assignments.find((assignment) => (
  assignment.id !== ignoreId && assignmentKey(assignment) === assignmentKey(candidate)
));

const persistAssignments = () => {
  if (storageAvailable) sessionStorage.setItem("kinderflowSchoolAssignments", JSON.stringify(assignments));
};

const bilingualLabel = (signId) => {
  const sign = contentFor(signId);
  return sign ? `${sign.en} / ${sign.es}` : "Sign unavailable";
};

const populateChildren = ({ keepSelection = false } = {}) => {
  const previous = keepSelection ? childSelect.value : "";
  const options = [new Option("Choose a child", ""), ...(GROUPS[groupSelect.value]?.children || []).map((child) => new Option(child, child))];
  childSelect.replaceChildren(...options);
  if (previous && (GROUPS[groupSelect.value]?.children || []).includes(previous)) childSelect.value = previous;
};

const renderMaterialChoices = (selected = null) => {
  const selectedSet = new Set(selected || availableMaterialsFor(signSelect.value).filter((material) => material !== "story"));
  const controls = availableMaterialsFor(signSelect.value).map((material) => {
    const label = document.createElement("label");
    const input = document.createElement("input");
    const text = document.createElement("span");
    input.type = "checkbox";
    input.name = "materials";
    input.value = material;
    input.checked = selectedSet.has(material);
    text.textContent = MATERIAL_LABELS[material];
    label.append(input, text);
    return label;
  });
  materialChoices.replaceChildren(...controls);
};

const toggleChildSelector = ({ clear = false } = {}) => {
  const oneChild = selectedAudience() === "child";
  childPanel.hidden = !oneChild;
  childSelect.disabled = !oneChild;
  if (clear || !oneChild) childSelect.value = "";
};

const draftAssignment = () => ({
  id: editingAssignmentId || "",
  signId: signSelect.value,
  groupId: groupSelect.value,
  audienceType: selectedAudience(),
  childId: selectedAudience() === "child" ? childSelect.value : "",
  materials: normaliseMaterials(selectedMaterials())
});

const updateAssignmentSummary = () => {
  assignmentResult.hidden = true;
  const draft = draftAssignment();
  const sign = contentFor(draft.signId);
  const group = GROUPS[draft.groupId];
  const target = draft.audienceType === "child"
    ? draft.childId || "one child"
    : `the ${group.short} group`;
  assignmentSummary.textContent = `${bilingualLabel(draft.signId)} will be shared with ${target}.`;
  assignmentMaterialSummary.textContent = draft.materials.length
    ? draft.materials.map((material) => MATERIAL_LABELS[material]).join(" · ")
    : "No materials selected";
  const missingChild = draft.audienceType === "child" && !draft.childId;
  const missingMaterials = draft.materials.length === 0;
  assignmentSubmit.disabled = !sign || missingChild || missingMaterials;
  assignmentValidation.textContent = missingMaterials
    ? "Choose at least one material to continue."
    : missingChild ? "Choose a child to continue." : "";
  if (editingAssignmentId) {
    assignmentSubmit.textContent = "Save changes";
  } else {
    const ctaTarget = draft.audienceType === "child"
      ? draft.childId || "one child"
      : group.short;
    assignmentSubmit.textContent = `Share ${sign?.en || "sign"} with ${ctaTarget}`;
  }
  duplicatePanel.hidden = true;
  duplicateAssignmentId = null;
};

const createDefinition = (term, value) => {
  const wrapper = document.createElement("div");
  const dt = document.createElement("dt");
  const dd = document.createElement("dd");
  dt.textContent = term;
  if (typeof value === "string") dd.textContent = value;
  else dd.append(value);
  wrapper.append(dt, dd);
  return wrapper;
};

const createAssignmentCard = (assignment) => {
  const article = document.createElement("article");
  article.dataset.activeAssignment = "";
  article.dataset.assignmentId = assignment.id;
  article.tabIndex = -1;
  const main = document.createElement("div");
  main.className = "active-assignment-main";
  const type = document.createElement("span");
  type.className = "content-type-tag";
  type.textContent = "Sign";
  const title = document.createElement("h3");
  title.textContent = bilingualLabel(assignment.signId);
  const details = document.createElement("dl");
  details.className = "active-assignment-details";
  const group = GROUPS[assignment.groupId];
  const audience = assignment.audienceType === "child"
    ? `${group.label} · ${assignment.childId}`
    : `${group.label} · Everyone in the group`;
  const actionContext = `${bilingualLabel(assignment.signId)} assignment for ${audience}`;
  const chips = document.createElement("span");
  chips.className = "active-material-chips";
  normaliseMaterials(assignment.materials).forEach((material) => {
    const chip = document.createElement("span");
    chip.className = "material-chip";
    chip.textContent = MATERIAL_LABELS[material];
    chips.append(chip);
  });
  details.append(createDefinition("Audience", audience), createDefinition("Materials", chips));
  main.append(type, title, details);
  const actions = document.createElement("div");
  actions.className = "active-assignment-actions";
  const status = document.createElement("span");
  status.className = "status-pill status-ready";
  status.textContent = "Active";
  const edit = document.createElement("button");
  edit.className = "text-link-button";
  edit.type = "button";
  edit.dataset.editAssignment = assignment.id;
  edit.textContent = "Edit";
  edit.setAttribute("aria-label", `Edit ${actionContext}`);
  const remove = document.createElement("button");
  remove.className = "text-link-button";
  remove.type = "button";
  remove.dataset.removeAssignment = assignment.id;
  remove.textContent = "Remove";
  remove.setAttribute("aria-label", `Remove ${actionContext}`);
  actions.append(status, edit, remove);
  article.append(main, actions);
  return article;
};

const renderActiveAssignments = () => {
  if (!assignments.length) {
    const empty = document.createElement("article");
    empty.className = "active-assignment-empty";
    const title = document.createElement("h3");
    title.textContent = "No active assignments";
    const copy = document.createElement("p");
    copy.textContent = "Choose available content to share with one of your groups or families.";
    empty.append(title, copy);
    activeList.replaceChildren(empty);
    return;
  }
  activeList.replaceChildren(...assignments.map(createAssignmentCard));
};

const startEditingAssignment = (assignmentId) => {
  const assignment = assignments.find((item) => item.id === assignmentId);
  if (!assignment) return;
  editingAssignmentId = assignment.id;
  signSelect.value = assignment.signId;
  groupSelect.value = assignment.groupId;
  renderMaterialChoices(assignment.materials);
  document.querySelector(`input[name="audience"][value="${assignment.audienceType}"]`).checked = true;
  populateChildren();
  toggleChildSelector();
  if (assignment.audienceType === "child") childSelect.value = assignment.childId;
  cancelEdit.hidden = false;
  assignmentResult.hidden = true;
  duplicatePanel.hidden = true;
  updateAssignmentSummary();
  assignmentForm.scrollIntoView({ behavior: preferredScrollBehavior, block: "start" });
  materialChoices.querySelector("input")?.focus({ preventScroll: true });
};

const resetAssignmentForm = ({ preserveGroup = true } = {}) => {
  const group = preserveGroup ? groupSelect.value : "Group 1–2";
  editingAssignmentId = null;
  signSelect.value = "more";
  groupSelect.value = group;
  document.querySelector('input[name="audience"][value="group"]').checked = true;
  populateChildren();
  toggleChildSelector({ clear: true });
  renderMaterialChoices();
  cancelEdit.hidden = true;
  duplicatePanel.hidden = true;
  assignmentResult.hidden = true;
  updateAssignmentSummary();
};

if (assignmentForm) {
  renderMaterialChoices();
  populateChildren();
  toggleChildSelector();
  renderActiveAssignments();
  updateAssignmentSummary();

  groupSelect.addEventListener("change", () => {
    populateChildren();
    toggleChildSelector({ clear: true });
    updateAssignmentSummary();
  });
  signSelect.addEventListener("change", () => {
    renderMaterialChoices();
    updateAssignmentSummary();
  });
  materialChoices.addEventListener("change", updateAssignmentSummary);
  document.querySelectorAll('input[name="audience"]').forEach((input) => input.addEventListener("change", () => {
    toggleChildSelector({ clear: true });
    updateAssignmentSummary();
  }));
  childSelect.addEventListener("change", updateAssignmentSummary);

  document.querySelectorAll("[data-select-library-sign]").forEach((button) => {
    button.addEventListener("click", () => {
      editingAssignmentId = null;
      signSelect.value = button.dataset.selectLibrarySign;
      renderMaterialChoices();
      cancelEdit.hidden = true;
      assignmentResult.hidden = true;
      updateAssignmentSummary();
      assignmentForm.scrollIntoView({ behavior: preferredScrollBehavior, block: "start" });
      groupSelect.focus({ preventScroll: true });
    });
  });

  assignmentForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const draft = draftAssignment();
    updateAssignmentSummary();
    if (assignmentSubmit.disabled) return;
    const duplicate = findExactDuplicate(draft, editingAssignmentId);
    if (duplicate) {
      duplicateAssignmentId = duplicate.id;
      duplicatePanel.hidden = false;
      assignmentResult.hidden = true;
      duplicatePanel.focus();
      return;
    }
    if (editingAssignmentId) {
      const index = assignments.findIndex((assignment) => assignment.id === editingAssignmentId);
      if (index === -1) return;
      assignments[index] = { ...draft, id: editingAssignmentId };
      assignmentStatus.textContent = `${bilingualLabel(draft.signId)} assignment updated.`;
    } else {
      const id = nextAssignmentId();
      assignments.push({ ...draft, id });
      const recipient = draft.audienceType === "child" ? draft.childId : GROUPS[draft.groupId].short;
      assignmentStatus.textContent = `${bilingualLabel(draft.signId)} was shared with ${recipient}.`;
    }
    persistAssignments();
    renderActiveAssignments();
    editingAssignmentId = null;
    cancelEdit.hidden = true;
    updateAssignmentSummary();
    assignmentResult.hidden = false;
    duplicatePanel.hidden = true;
    assignmentResult.focus();
  });

  assignAnother.addEventListener("click", () => {
    resetAssignmentForm();
    signSelect.focus();
  });
  cancelEdit.addEventListener("click", () => {
    resetAssignmentForm();
    signSelect.focus();
  });
  document.querySelector("#view-active-assignment").addEventListener("click", () => {
    const card = [...activeList.querySelectorAll("[data-assignment-id]")]
      .find((item) => item.dataset.assignmentId === duplicateAssignmentId);
    card?.scrollIntoView({ behavior: preferredScrollBehavior, block: "center" });
    card?.focus({ preventScroll: true });
  });
  document.querySelector("#change-assignment-materials").addEventListener("click", () => startEditingAssignment(duplicateAssignmentId));
}

activeList?.addEventListener("click", (event) => {
  const editButton = event.target.closest("[data-edit-assignment]");
  if (editButton) {
    startEditingAssignment(editButton.dataset.editAssignment);
    return;
  }
  const removeButton = event.target.closest("[data-remove-assignment]");
  if (!removeButton) return;
  const removed = assignments.find((assignment) => assignment.id === removeButton.dataset.removeAssignment);
  assignments = assignments.filter((assignment) => assignment.id !== removeButton.dataset.removeAssignment);
  if (editingAssignmentId === removeButton.dataset.removeAssignment) {
    editingAssignmentId = null;
    cancelEdit.hidden = true;
    renderMaterialChoices();
  }
  if (duplicateAssignmentId === removeButton.dataset.removeAssignment) {
    duplicateAssignmentId = null;
    duplicatePanel.hidden = true;
  }
  persistAssignments();
  renderActiveAssignments();
  updateAssignmentSummary();
  assignmentStatus.textContent = removed ? `${bilingualLabel(removed.signId)} was removed from active assignments.` : "";
  assignmentResult.hidden = false;
  assignmentResult.focus();
});

const reviewedDelivery = (() => {
  if (typeof window === "undefined" || new URLSearchParams(window.location.search).get("reviewed") !== "1" || !storageAvailable) return null;
  try {
    const value = JSON.parse(sessionStorage.getItem("kinderflowReviewedContentPack") || "null");
    return value?.review_status === "APPROVED" && value?.human_review?.approved === true ? value : null;
  } catch (_error) {
    return null;
  }
})();

if (assignmentForm && typeof window !== "undefined") {
  const parameters = new URLSearchParams(window.location.search);
  const requestedSign = String(reviewedDelivery?.sign_id || parameters.get("sign") || "").trim().toLowerCase();
  if (requestedSign && contentFor(requestedSign)) {
    signSelect.value = requestedSign;
    renderMaterialChoices();
    updateAssignmentSummary();
    if (reviewedDelivery) assignmentValidation.textContent = `${bilingualLabel(requestedSign)} is ready to share with your groups or families.`;
  } else if (requestedSign) {
    const unsupportedOption = new Option(`${requestedSign.toUpperCase()} — Not available`, "__unsupported__", true, true);
    signSelect.prepend(unsupportedOption);
    signSelect.value = "__unsupported__";
    renderMaterialChoices([]);
    updateAssignmentSummary();
    assignmentSummary.textContent = "Choose an available sign to continue.";
    assignmentValidation.textContent = "This reviewed sign is not available in your nursery content.";
  }
}

const addonForm = document.querySelector("#school-addon-form");
const addonSelect = document.querySelector("#school-addon");
const addonAction = document.querySelector("#school-addon-action");
const addonScope = document.querySelector("#school-addon-scope");
const addonTarget = document.querySelector("#school-addon-target");
const addonSubmit = document.querySelector("#school-addon-submit");
const addonStatus = document.querySelector("#school-addon-status");

if (addonForm) {
  const groups = Object.values(GROUPS).map((group) => group.label);
  const children = Object.values(GROUPS).flatMap((group) => group.children);
  const updateAddonLabel = () => {
    const verb = addonAction.value === "enabled" ? "Enable" : "Disable";
    addonSubmit.textContent = `${verb} ${addonSelect.value} for ${addonTarget.value}`;
    addonStatus.textContent = "";
  };
  const populateAddonTargets = () => {
    const targets = addonScope.value === "child" ? children : groups;
    addonTarget.replaceChildren(...targets.map((target) => new Option(target, target)));
    updateAddonLabel();
  };
  addonAction.addEventListener("change", updateAddonLabel);
  addonSelect.addEventListener("change", updateAddonLabel);
  addonScope.addEventListener("change", populateAddonTargets);
  addonTarget.addEventListener("change", updateAddonLabel);
  addonForm.addEventListener("submit", (event) => {
    event.preventDefault();
    addonStatus.textContent = `${addonSelect.value} ${addonAction.value} for ${addonTarget.value}.`;
  });
  populateAddonTargets();
}
