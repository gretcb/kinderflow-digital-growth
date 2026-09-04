(() => {
  "use strict";

  const page = (window.location.pathname.split("/").pop() || "index.html").toLowerCase();

  // Protected technical route:
  // Create Sign contains the validated MediaPipe videos, metrics, charts,
  // pose evidence and reference-frame workflow. This layer must not touch it.
  if (page === "create-sign.html" || page === "print-card.html") return;

  const pages = {
    "index.html": { profile: "platform", label: "KinderFlow", title: "Product overview" },
    "admin.html": { profile: "company", label: "KinderFlow team", title: "Company workspace" },
    "content-studio.html": { profile: "company", label: "KinderFlow team", title: "Content Studio" },
    "library.html": { profile: "company", label: "KinderFlow team", title: "Content Library" },
    "flashcards.html": { profile: "company", label: "KinderFlow team", title: "Family materials" },
    "create-story.html": { profile: "company", label: "KinderFlow team", title: "Story creator" },
    "create-song.html": { profile: "company", label: "KinderFlow team", title: "Songs · Coming soon" },
    "school.html": { profile: "school", label: "Little Steps Nursery", title: "Nursery workspace" },
    "family.html": { profile: "family", label: "Family view", title: "Your Kinder Signs" }
  };

  const config = pages[page];
  if (!config) return;

  const body = document.body;
  const main = document.querySelector("main");
  const header = document.querySelector(".site-header");

  body.classList.add("product-shell");
  body.dataset.profile = config.profile;

  if (main && !main.id) main.id = "main-content";

  const skip = document.createElement("a");
  skip.className = "product-skip-link";
  skip.href = "#main-content";
  skip.textContent = "Skip to main content";
  body.prepend(skip);

  if (header && config.profile !== "platform" && !document.querySelector(".role-context-bar")) {
    const bar = document.createElement("div");
    bar.className = "role-context-bar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Current product profile");

    const copy = document.createElement("div");
    copy.className = "role-context-copy";

    const kicker = document.createElement("span");
    kicker.className = "role-context-kicker";
    kicker.textContent =
      config.profile === "company" ? "Company profile" :
      config.profile === "school" ? "Nursery profile" : "Family profile";

    const label = document.createElement("strong");
    label.textContent = config.label;

    const separator = document.createElement("span");
    separator.className = "role-context-separator";
    separator.setAttribute("aria-hidden", "true");
    separator.textContent = "·";

    const title = document.createElement("span");
    title.className = "role-context-task";
    title.textContent = config.title;

    copy.append(kicker, label, separator, title);

    const switchLink = document.createElement("a");
    switchLink.href = "index.html";
    switchLink.className = "role-context-switch";
    switchLink.textContent = "View another profile";

    bar.append(copy, switchLink);
    header.insertAdjacentElement("afterend", bar);
  }

  document.querySelectorAll(".prototype-boundary").forEach((note) => {
    if (note.closest("details") || note.dataset.productDisclosure === "done") return;

    const details = document.createElement("details");
    details.className = "product-disclosure";

    const summary = document.createElement("summary");
    summary.textContent = "Demo details";

    const content = document.createElement("div");
    content.className = "product-disclosure-content";
    while (note.firstChild) content.append(note.firstChild);

    note.dataset.productDisclosure = "done";
    details.append(summary, content);
    note.replaceWith(details);
  });
})();
