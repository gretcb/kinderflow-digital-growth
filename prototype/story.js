"use strict";

const ROUTINES = {
  snack: { label: "Snack time", phrase: "snack time", title: "A little more?", object: "pear" },
  bedtime: { label: "Bedtime", phrase: "bedtime", title: "One more story", object: "story" },
  dressing: { label: "Getting dressed", phrase: "getting dressed", title: "One more sock", object: "sock" },
  playtime: { label: "Playtime", phrase: "playtime", title: "One more piece", object: "block" }
};

const form = document.querySelector("#story-form");
const preview = document.querySelector("#story-preview");
const heading = document.querySelector("#story-heading");
const body = document.querySelector("#story-body");
const meta = document.querySelector("#story-meta");
const stateLabel = document.querySelector("#story-state");
const wordCount = document.querySelector("#word-count");
const reviewStatus = document.querySelector("#story-review-status");
const steps = Array.from(document.querySelectorAll("[data-story-step]"));

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

const buildStory = ({ routine, length, tone }) => {
  const context = ROUTINES[routine];
  const middle = tone === "playful"
    ? "She looked at Dad, smiled and used the MORE sign."
    : tone === "reassuring"
      ? "She looked calmly at Dad and used the MORE sign."
      : "She looked at Dad and used the MORE sign.";
  const opening = routine === "snack"
    ? `Lina finished her pieces of ${context.object}.`
    : `Lina was enjoying ${context.phrase}.`;
  const shortEnding = "“Would you like more?” Dad asked. Lina smiled and Dad repeated the MORE sign.";
  const longEnding = `“Would you like more?” Dad asked. Lina smiled. Dad continued ${context.phrase} and repeated the MORE sign. They finished the routine without rushing.`;
  return {
    context,
    title: context.title,
    text: `${opening} ${middle} ${length === "very-short" ? shortEnding : longEnding}`
  };
};

if (form) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const values = Object.fromEntries(new FormData(form));
    const story = buildStory(values);
    heading.textContent = story.title;
    body.textContent = story.text;
    meta.textContent = `MORE · ${story.context.label} · ${values.age} · English`;
    const count = story.text.trim().split(/\s+/).length;
    wordCount.textContent = `${count} words · ${values.length === "very-short" ? "very-short" : "short"} limit met`;
    reviewStatus.textContent = "Evaluation complete. Draft is ready for human review.";
    setState("review", "Ready for human review");
    preview.focus();
  });
}

document.querySelector("#approve-story")?.addEventListener("click", () => {
  setState("published", "Published");
  reviewStatus.textContent = "Approved by the prototype reviewer and marked Published locally. Nothing was sent or saved.";
});

document.querySelector("#request-story-changes")?.addEventListener("click", () => {
  setState("review", "Changes requested");
  reviewStatus.textContent = "Changes requested. The draft remains unpublished.";
});

document.querySelector("#keep-story-draft")?.addEventListener("click", () => {
  setState("draft", "Draft");
  reviewStatus.textContent = "Kept as draft. Nothing was published.";
});
