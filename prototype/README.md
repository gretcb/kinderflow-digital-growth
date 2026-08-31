# Kinder Signs static prototype

This dependency-free prototype shows the user-facing Kinder Signs product and its commercial logic. It is a product demonstration, not the internal Computer Vision or LLM workflow.

It also includes `admin.html`, a separate internal prototype showing how KinderFlow could register adult reference material, inspect motion diagnostics, govern future rendering preparation, review library content and assign it to example school groups. The admin page is illustrative and does not upload, process, publish or integrate data.

## How to open

Option 1 — open the file directly:

```text
open prototype/index.html
```

Option 2 — serve it locally:

```bash
cd prototype
python -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000).

- School-family view: [http://localhost:8000/index.html](http://localhost:8000/index.html)
- Internal admin view: [http://localhost:8000/admin.html](http://localhost:8000/admin.html)

The page uses `data/approved_sign_more.json` when served over HTTP. It includes equivalent fallback data in `app.js`, so the interactions also work when `index.html` is opened directly with a `file://` URL.

## What the prototype demonstrates

### School-facing flow

The prototype shows a school selecting a studied sign from the Kinder Signs library, assigning the weekly sign to a classroom group, child profile or tutor profile, and preparing a family output for its existing school-family channel.

The distribution actions are deliberately channel-neutral: copy a message, export the routine card through the browser print dialog, or prepare a prototype share-link state. Kinder Signs does not replace a school communication app.

### Tutor and family flow

Two main tutors receive the weekly sign, short guidance for modelling it naturally, a school-home connection and clear boundaries. Families can extend access to a grandparent, nanny or second home as an optional paid add-on.

### Monetization hypothesis

The base access model includes two main tutors. Incremental value can come from:

- extra caregiver invitations;
- printed flashcards;
- original Kinder Signs mini stories;
- original Kinder Signs short songs; and
- routine packs for recurring school and home contexts.

All story and song concepts are original Kinder Signs content linked to the weekly sign and its routine. No third-party characters, brands, songs or stories are used.

## What is not implemented

This is a static feasibility prototype. It does not include:

- accounts, login or permissions;
- a database or saved profiles;
- live school communication integrations;
- real share links or message delivery;
- payment or checkout;
- API calls, analytics or tracking;
- video playback or PDF generation beyond the browser print dialog; or
- a production content-management system.

## Privacy and governance boundaries

No real child data is included, and no child video is required. The child profile is explicitly an example. All page data stays in local static files.

KinderFlow may use Computer Vision to support motion representation and an LLM to support content drafting internally. These systems do not validate final sign correctness. Human review and controlled library operations remain KinderFlow responsibilities; the school does not manage the AI workflow. The family card is general routine guidance, not clinical advice.
