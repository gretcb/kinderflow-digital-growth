# Kinder Signs static prototype

This dependency-free prototype shows the Kinder Signs school-home experience and its commercial logic. Kinder Signs is not another sign dictionary: the school uses one approved sign in a real routine, and the family receives the same short guidance at home.

It also includes `admin.html`, a separate internal prototype showing how Kinder Signs could create an approved sign video, run a movement quality check, prepare a family card, complete expert review and add the approved sign card to its library. The school-delivery view follows the hierarchy `school account → classroom group → teacher → child profile → family access / packs`. All controls and profiles are illustrative; the page does not save, process, publish or integrate data.

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

### Reference video and avatar preparation

The internal admin view registers a Kinder Signs reference video, shows the existing movement-check evidence, records the movement data/skeleton step and turns the visual direction into a short guide brief. The character defines the look; the reference movement defines the sign. No child video is used.

The avatar preview is the next build, not a finished feature. Final validated avatar generation is not implemented, and expert review remains required. This internal workflow belongs to Kinder Signs; the school only selects approved library items and assigns them to groups or children.

### School-facing flow

The prototype shows School A on the Kinder Signs Basic plan, Group A for ages 1–2 years and Teacher 1. The educator selects an already approved weekly sign and assigns it either to the whole group or to one example child. The family receives the same approved guidance at home. The school does not create the video, prepare the content or manage the internal workflow.

The child roster makes active access visible to the teacher/admin:

- Child A has two parent profiles, flashcards and extra caregiver access;
- Child B has one parent profile and base access only; and
- Child C has two parent profiles and flashcards.

The prepared output follows the active access attached to each child or family. A group assignment prepares the base family card for all active children and includes premium materials only where those materials are active.

The distribution actions are deliberately channel-neutral: copy a message, export the routine card through the browser print dialog, or prepare a prototype share-link state. Kinder Signs does not replace a school communication app.

### Tutor and family flow

Two main tutors receive the weekly sign, short guidance for using it naturally in the same home routine and clear boundaries. Families can extend access to a grandparent, nanny or second home as an optional paid add-on.

### Monetization hypothesis

The base access model includes two main tutors. Premium packs can be active for a whole group or an individual child, while extra caregiver access remains linked to a child’s family. Incremental value can come from:

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
- billing, charges or payment-state management;
- live school communication integrations;
- real share links or message delivery;
- payment or checkout;
- API calls, analytics or tracking;
- video playback or PDF generation beyond the browser print dialog; or
- a production content-management system.

## Privacy and governance boundaries

No real child data is included, and no child video is required. All page data stays in local static files.

KinderFlow may use Computer Vision for movement quality checks and an LLM to help draft family cards. These tools do not confirm final sign correctness. Expert review and library management remain KinderFlow responsibilities; the school does not manage the AI workflow. Family cards are linked to school routines, do not provide clinical advice and do not promise faster development.
