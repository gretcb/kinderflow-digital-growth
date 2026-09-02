"use strict";

const operationsBody = document.querySelector("#operations-body");
const reviewPanel = document.querySelector("#operations-review");
const actionStatus = document.querySelector("#operations-action-status");
let operationsResults = [];
let selectedOperation = null;

const setOperationText = (selector, value) => { document.querySelector(selector).textContent = value; };

const renderOperationsReview = (item) => {
  selectedOperation = item;
  setOperationText("#review-sign-title", item.display_name);
  setOperationText("#review-source", item.source_reference || "Not attached");
  setOperationText("#review-technical", item.technical);
  setOperationText("#review-content", item.content);
  setOperationText("#review-artwork", item.artwork);
  setOperationText("#review-hand", item.hand_review);
  setOperationText("#review-gate", item.quality_gate);
  setOperationText("#review-llm", item.llm);
  setOperationText("#review-publication", item.publication);
  const libraryStatus = document.querySelector("#review-library-status");
  libraryStatus.textContent = item.library;
  libraryStatus.className = `status-pill ${item.library === "Blocked" ? "status-review" : "status-ready"}`;
  const blockers = document.querySelector("#review-blockers");
  blockers.replaceChildren(...item.blocking_reasons.map((reason) => {
    const listItem = document.createElement("li");
    listItem.textContent = reason;
    return listItem;
  }));
  actionStatus.textContent = item.library === "Blocked"
    ? "Approval is blocked until the listed policy requirements are complete."
    : "Ready for explicit human review.";
  reviewPanel.focus({ preventScroll: true });
};

const renderOperationsTable = () => {
  operationsBody.replaceChildren(...operationsResults.map((item) => {
    const row = document.createElement("tr");
    [item.display_name, item.source, item.technical, item.content, item.artwork, item.hand_review, item.quality_gate, item.human_review, item.library].forEach((value, index) => {
      const cell = document.createElement(index === 0 ? "th" : "td");
      if (index === 0) cell.scope = "row";
      cell.textContent = value;
      row.append(cell);
    });
    const detailCell = document.createElement("td");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "text-link-button";
    button.dataset.reviewSign = item.sign_id;
    button.textContent = "Review";
    detailCell.append(button);
    row.append(detailCell);
    return row;
  }));
};

operationsBody.addEventListener("click", (event) => {
  const button = event.target.closest("[data-review-sign]");
  if (!button) return;
  const item = operationsResults.find((candidate) => candidate.sign_id === button.dataset.reviewSign);
  if (item) renderOperationsReview(item);
});

document.querySelector("#review-approve").addEventListener("click", () => {
  if (!selectedOperation) return;
  actionStatus.textContent = selectedOperation.library === "Blocked"
    ? "Approval rejected: publication policy still has blocking reasons."
    : "Approval would require a persisted human-review record; this static screen does not create one.";
});

document.querySelector("#review-request-changes").addEventListener("click", () => {
  actionStatus.textContent = selectedOperation
    ? `Changes requested locally for ${selectedOperation.display_name}. No production record was changed.`
    : "Select a sign first.";
});

document.querySelector("#review-rebuild-visual").addEventListener("click", () => {
  actionStatus.textContent = selectedOperation
    ? `Visual rebuild remains blocked for ${selectedOperation.display_name} until official character and reviewed hand assets exist.`
    : "Select a sign first.";
});

const loadOperations = async () => {
  try {
    const response = await fetch("data/content_operations.json", { cache: "no-store" });
    if (!response.ok) throw new Error("Readiness report unavailable.");
    const report = await response.json();
    if (!Array.isArray(report.results) || report.results.length !== 5) throw new Error("Readiness report schema is invalid.");
    operationsResults = report.results;
    renderOperationsTable();
    renderOperationsReview(operationsResults[0]);
  } catch (error) {
    operationsBody.innerHTML = `<tr><td colspan="10">${error.message} Run the local regression command and reload.</td></tr>`;
    actionStatus.textContent = "Run python -m content_ops to rebuild the local readiness report.";
  }
};

loadOperations();
