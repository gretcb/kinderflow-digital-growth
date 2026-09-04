# Content Operations, explained simply

Content Operations is not another AI feature. It is the set of rules and records that keeps source evidence, family wording, artwork, review and publication from being mixed together.

## Why we added states

A sign is not simply “done” or “not done.” Its video may have been processed while its artwork is missing. Its family wording may be ready for review while nobody has approved publication.

States make those differences visible. For MORE, the current local record says:

- source: review needed;
- technical evidence: review needed;
- family content: ready for review;
- artwork: needs artwork;
- hand review: needs review;
- publication: draft and blocked.

This is more honest than one green “ready” badge.

## Why technical, content, visual and publication status are separate

- **Technical status** answers: did the video produce usable movement evidence?
- **Content status** answers: is the family wording drafted, reviewed or approved?
- **Visual status** answers: are the character and sign-specific hands ready and reviewed?
- **Publication status** answers: has the complete version passed its controlled release steps?

A technical pass cannot approve family wording or artwork. A good illustration cannot repair missing movement evidence.

## Why we keep provenance

Provenance means knowing what each output came from. For one MORE item, we want to be able to answer:

- Which reference was used?
- Which CV evidence was linked?
- Which structured content version was rendered?
- Which character and hand assets were used?
- Which review decision applied?
- Which exact package was released?

The current MORE record deliberately says its source identity still needs confirmation.

## What hashes are used for

A SHA-256 hash is a digital fingerprint. The content-operations test records fingerprints for the current `signs.json` and POC summary. The summary is the versioned WATER artifact; its link from the older blocked MORE package is a known identity mismatch and must not support a MORE technical claim. The separate local MORE demonstration is ignored run evidence. If a hashed input changes, its fingerprint changes and the old provenance check no longer matches.

The hash does not prove ownership, correctness or security by itself. It only helps detect a change.

## Why we have an audit log

The local audit helper records important events in order, for example:

```text
package prepared
→ quality gate checked
→ artwork attached
→ hand reviewed
→ human approval recorded
```

This helps answer “what happened?” The current JSON Lines log is a local engineering mechanism, not a tamper-proof production audit service.

## What a publication package is

A publication package is a set of versioned JSON records that points to one combination of source, content, visual assets and review state. It prevents an approval for one version being silently applied to a later changed version.

The repository can build this package consistently. The current MORE package is draft and blocked; it is evidence of packaging behaviour, not an approved sign.

## Why create a five-sign regression set

MORE, EAT, WATER, ALL DONE and HELP form a small stable engineering set. Every time the rules change, all five are checked again. This catches broken schemas, missing evidence and accidental changes to readiness logic.

It is not a linguistic benchmark. Today, all five pass their schema checks and all five remain blocked from the library for stated reasons.

## Why publication requires human approval

MediaPipe can show whether landmarks were captured. Code can show whether a required field exists. Neither can decide that a sign and its family material are professionally suitable for release.

The state machine therefore blocks `DRAFT → PUBLISHED`. Publication requires the intermediate review and approval states plus an explicit human approval record.

## Why this matters outside the bootcamp

A commercial content service needs repeatable answers to basic operating questions:

- What exactly are we offering to schools?
- Which evidence supports it?
- Has the hand artwork been reviewed?
- Which version did a school receive?
- Why is an item blocked?
- Can we rerun the same operation without making duplicates?

Content Operations starts to answer those questions without pretending the prototype is a full production CMS.
