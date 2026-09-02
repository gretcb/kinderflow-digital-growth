# Privacy facts

This is a data-minimisation inventory for later GDPR work. It is not a GDPR certification.

## DATA CURRENTLY USED

| Data | Why it exists | Current handling |
|---|---|---|
| Local adult reference video | Source for movement extraction | Processed locally; input and run media are excluded from Git |
| Hand and pose landmarks | Structured technical evidence | Stored in local POC/MVP run artifacts; canonical CSV evidence is excluded from public Git |
| Capture diagnostics | Explain coverage, gaps and technical status | Small non-sensitive JSON/plots are retained as evidence |
| Sign name, routine and family copy | Build content and printable output | Local structured JSON |
| Source reference and technical run ID | Link an asset to its evidence | Synthetic/controlled identifiers; no raw path shown in the UI |
| File hashes | Detect changes in referenced local artifacts | Stored in manifests; they do not establish ownership or correctness |
| Content-operations events | Record local system/workflow events | System/synthetic identifiers; no reviewer name or child data |
| Fictional school/child labels | Demonstrate assignment UX | Static examples such as School A and Child A; not real records |

## DATA NOT REQUIRED

| Data | Why it is not required for the core workflow |
|---|---|
| Child video or photograph | The CV use case processes controlled reference material, not child performance |
| Child name or surname | Content production and template rendering do not need identity |
| Health or developmental data | Kinder Signs does not diagnose, score or personalise clinical support |
| Emotion or biometric identification | Not part of the intended purpose |
| Family message content | The prototype prepares output but does not integrate with a communication channel |
| Payment details | Billing is not implemented |

## POTENTIAL FUTURE PILOT DATA

| Field | Why it would exist | What should be minimised |
|---|---|---|
| `event_id` | Deduplicate and trace a product event | Use a random ID with no embedded personal data |
| `timestamp` | Order actions and measure task duration | Limit precision/retention to what the metric needs |
| `event_type` | Count a defined action | Use an allow-list; no free-text activity description |
| `school_id` | Measure adoption by participating school | Use a synthetic/pseudonymous code in analysis data |
| `group_id` | Measure group assignment | Do not include group names unless operationally necessary |
| `family_id` | Measure delivery/reach without names | Use a short-lived pseudonymous ID; avoid child linkage where possible |
| `sign_id` / content type | Attribute use to a library item | No personal data is needed |
| `duration_ms` | Estimate educator/reviewer effort | Store task duration, not detailed staff monitoring |
| minimal metadata | Explain the specific event | No names, media, health fields, developmental notes or unrestricted free text |

## Decisions needed before a real pilot

- Define controller/processor roles and every vendor receiving data.
- Confirm the lawful basis and participant notices.
- Decide whether family-level IDs are necessary or whether aggregates are enough.
- Set access, retention, deletion, backup and incident rules.
- Decide whether a DPIA is required for the actual pilot design.
- Prevent prototype fields from becoming production data collection by default.
