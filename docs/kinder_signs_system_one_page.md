# Kinder Signs system in one page

This is an evidence summary, not final submission copy.

## Problem

Some nursery schools use signs in class, while families may receive little or mismatched guidance for using the same sign at home. Existing content does not automatically create continuity between a school routine and family practice.

## Solution

Kinder Signs is a school-led Signs & Flashcards Library. Kinder Signs prepares and governs the content centrally. An educator selects an available sign and assigns it to a group or child. The family receives the matching short guidance and printable material.

## How it works

```text
Validated reference video
→ movement extraction and technical checks
→ content and visual preparation
→ human review
→ published library item
→ school assignment
→ family output
```

One published source can support a video interface, flashcards and later approved derivative content. The school does not upload reference videos or manage the production workflow.

## AI role

- Computer Vision turns observed reference movement into landmarks, a skeleton preview and technical diagnostics.
- An LLM may help draft short family wording from supplied source content.
- LangSmith can trace and evaluate only that LLM-assisted wording.
- n8n can move structured information through defined workflow steps.

AI does not certify sign correctness or publish content on its own.

## Human role

A qualified person must confirm the source and content before publication. Human control is also required when technical evidence needs interpretation. The repository models this gate but does not implement production reviewer identity or authentication.

## School role

The school selects from content it is entitled to use, assigns it to groups or a fictional child profile, and uses it in routines. It does not create videos, run Computer Vision or approve master content.

## Family role

Families receive the same sign label, routine context, short guidance and optional printable material. The family view contains no technical AI language and makes no clinical or developmental claim.

## What is working today

- Local MP4 upload and the existing MediaPipe processing pipeline.
- Run-specific landmarks, diagnostics, metrics and landmark-overlay video.
- A reproducible sample path for the known reference video.
- A deterministic Flashcard Studio with Spanish/English content, three layouts, A6/A5 options and browser print.
- Deterministic content, asset and publication checks with automated tests.
- A five-sign engineering regression set and versioned local package output.
- A keyless LangSmith dry-run and deterministic LLM-output quality gate.

## What is still pending

- Confirmed source rights, sign identity and professional review for publishable material.
- Final character artwork and reviewed sign-specific hand assets.
- Production avatar generation and movement-fidelity testing.
- Persistent publishing, user accounts, permissions, hosted storage and integrations.
- Live LangSmith evidence and a tested n8n runtime execution for content operations.
- Real school/family use and commercial evidence.

## What the pilot must prove

- Educators can assign content with little additional effort.
- Families open and use the material.
- Several signs can pass through the same controlled production process.
- Technical capture works across more references and conditions.
- Professional review is operationally feasible.
- A school payer sees enough value to continue and the economics are credible.

No real pilot has taken place yet.
