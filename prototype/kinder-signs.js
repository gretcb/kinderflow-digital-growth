"use strict";

const videoSlots = [...document.querySelectorAll("[data-video-slot]")];

const unavailableMessage = (slot) => {
  slot.replaceChildren();
  const label = document.createElement("strong");
  label.className = "ks-video-title";
  label.textContent = "Video tutorial";
  const message = document.createElement("p");
  message.textContent = "Video tutorial not available yet. Use the Flashcard or Routine Card instead.";
  slot.append(label, message);
};

const renderVideo = (slot, record) => {
  slot.replaceChildren();

  const label = document.createElement("strong");
  label.className = "ks-video-title";
  label.textContent = "Baby Sign video tutorial";

  const video = document.createElement("video");
  video.controls = true;
  video.playsInline = true;
  video.preload = "metadata";
  video.src = record.url;
  video.setAttribute("aria-label", `${record.label || record.sign_id} Baby Sign video preview`);

  video.addEventListener("error", () => unavailableMessage(slot), { once: true });
  slot.append(label, video);
};

const normalizeCatalog = (payload) => {
  if (payload?.signs && !Array.isArray(payload.signs)) return payload.signs;
  if (Array.isArray(payload?.signs)) {
    return Object.fromEntries(payload.signs.map((record) => [record.sign_id, record]));
  }
  return {};
};

const loadVideoCatalog = async () => {
  try {
    const response = await fetch("/api/illustrative-videos", { cache: "no-store" });
    if (!response.ok) throw new Error("Video catalogue unavailable");
    const catalog = normalizeCatalog(await response.json());

    videoSlots.forEach((slot) => {
      const record = catalog[slot.dataset.videoSlot];
      if (record?.available && record?.url) renderVideo(slot, record);
      else unavailableMessage(slot);
    });
  } catch (_error) {
    videoSlots.forEach(unavailableMessage);
  }
};

loadVideoCatalog();
