# KinderFlow plain-language UX audit

Date: 3 September 2026

## Scope and method

This audit covers the eleven current prototype routes, including the dedicated print-proof route, and the JavaScript that writes copy into them. Primary UI now leads with the user’s task and decision. Internal keys, API fields, stored state values and test fixtures remain unchanged; JavaScript presentation maps translate those values for display.

Technical evidence is available only to KinderFlow Admin users through disclosures labelled **Technical and source details**. School and Family views contain product and routine language only.

## Route audit

| Route | Role and primary user | Primary task | Internal wording found | Plain-language result | Changed | Technical detail | Deferred |
|---|---|---|---|---|---|---|---|
| `index.html` | KinderFlow Hub; prospective schools and product reviewers | Understand the product and choose a view | Computer Vision, MediaPipe, generative architecture, capstone prototype | Explains trusted references, consistent formats and human review | Yes | Removed from this public surface | Broader Hub information architecture remains Prompt 6A |
| `admin.html` | KinderFlow Admin; internal operator | Open content, school and activity workspaces | Static prototype, bounded operational signals, illustrative metrics | Uses operations, example activity and a single truthful example-data boundary | Yes | Not needed on this route | Live analytics remain outside the MVP |
| `content-studio.html` | KinderFlow Admin; content operator | Choose a top-level workspace | Direct Flashcard/Story/Song tools and implementation-first descriptions | Uses Studio overview, Create sign, Master Library and Schools; family formats are derived outputs | Yes | Method details remain in a **Technical and source details** disclosure | Library architecture remains Prompt 5 |
| `create-sign.html` | KinderFlow Admin; sign operator and reviewer | Choose a sign/reference, review the reference, choose a visual and create family materials | Processing, technical review, landmarks, grounded fallback, visual package/candidate, internal printable, raw run state | Uses the nine-step product journey, reference review, reviewed references, visual options and family materials | Yes | Raw status, metrics, source/run data and Open Peeps provenance remain in **Technical and source details** | MediaPipe extraction is unchanged |
| `library.html` | KinderFlow Admin; content and library reviewer | Review content readiness and prepare family wording | Raw generation labels, JSON, deterministic gate, LangSmith, component filenames and policy states | Uses AI-assisted draft, approved source copy, quality checks and clear readiness labels | Yes | Raw structured output, review trace, component metadata and operations report remain in **Technical and source details** disclosures | Master Content Library redesign remains Prompt 5 |
| `flashcards.html` | KinderFlow Admin; printable reviewer | Choose a reviewed sign, card/language, approve and print | Eligible/internal proof, grounded visual package, not ready | Uses Finish your printable, Ready for approval, Back to visual options and Bilingual/Spanish | Yes | Internal stored approval values remain hidden | Final saved-PDF visual QA remains |
| `print-card.html` | KinderFlow Admin; printable reviewer | Review the A5 proof and open Print / Save as PDF | Internal printable in status, accessible name and card footer | Uses printable proof consistently | Yes | Internal stored approval values remain hidden | Final saved-PDF visual QA remains Prompt 4 |
| `create-story.html` | KinderFlow Admin; story author and reviewer | Choose story details, create an English or Spanish draft and review it | Structured prompt, evaluator score, LLM/n8n/LangSmith flow, misleading Published label | Uses story details, story checks, human review and approved locally | Yes | Architecture and evaluation tooling remain in **Technical and source details** | Catalan remains Prompt 4 |
| `create-song.html` | KinderFlow Admin; product/content planner | Understand the planned Song format | P3 extensibility and implementation-dependency wording | Uses planned format, coming later and a clear future review path | Yes | Removed because no technical action is available | Song generation remains a later capability |
| `school.html` | School Admin; educator or school administrator | See plan content, share signs and manage family access | Operations, distribution, metrics and prototype phrasing | Uses Little Steps Nursery, your plan, available content, Share and active assignments | Yes | Demo disclosure is collapsed under **Demo details** | Production persistence remains outside the MVP |
| `family.html` | Family View; parent or caregiver | Understand the sign, routine and shared materials | Output preview, fictional/demo, implementation and publication boundaries | Uses shared by Little Steps Nursery, sign guidance, family materials and a clear help path | Yes | None exposed | Additional languages and final delivery remain outside the MVP |

## Presentation mappings

Representative display mappings include:

| Internal value or concept | Primary UI label |
|---|---|
| MediaPipe processing | Reference review |
| Landmark extraction | Find the reference poses |
| Technical review | Reference review |
| Dominant-hand landmark coverage | Main-hand visibility |
| Unresolved frames | Frames needing review |
| `KNOWLEDGE_REFERENCE_FALLBACK` | Reviewed references |
| Visual package | Sign visual |
| Candidate | Visual option |
| Approved for internal printable | Ready for family materials |
| `LLM_ASSISTED` | AI-assisted draft |
| `HUMAN` | Approved source copy |
| Deterministic quality gate | Quality checks |
| `DRY_RUN` | Demo mode, in details only |
| `NOT_APPLICABLE` | Not used for this step, in details only |

## Story language behavior

Story output supports English and Spanish. The selected language is shown in the preview metadata. Each language uses a complete, separate story variant so the output is not mixed. Changing language or any other brief field clears the previous story text, returns the flow to Draft, disables review actions and requires a new draft before approval.

## Sign and printable recovery behavior

Create a Sign resolves its illustration only from the explicit selected sign identity, preferring `run.sign.sign_id`. MORE, HELP, EAT, SLEEP, MILK and WATER are explicit choices. The included app demo selects and retains MORE; historical POC evidence remains WATER. A supported sign without a reviewed illustration shows a truthful not-ready message; an unknown sign shows an unsupported message. Neither state falls back to MORE.

Flashcard Studio distinguishes three cases: requested sign ready, requested sign awaiting visual review, and requested sign unsupported. An unsupported query never silently selects MORE. Normal first-sign selection remains only when no sign was requested.

## Accessibility and responsive checks

- Native labelled controls are retained.
- Status changes use `aria-live` regions already present in the routes.
- Visual options remain keyboard-operable radio controls with descriptive alternative text.
- Details summaries have visible keyboard focus.
- The nine-step sign journey reflows across desktop, tablet and mobile layouts.
- Existing reduced-motion, focus-visible, 44 px target and responsive rules remain in place.

Automated checks cover headings, duplicate IDs, labels, local links, prohibited primary-language terms, JavaScript syntax and bilingual Story output. A headless-browser render pass covered all 18 sign candidates and the three registered Open Peeps source examples; founder visual and sign-language review is still required.
