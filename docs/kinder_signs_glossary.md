# Kinder Signs glossary

| Term | Plain-language meaning | How Kinder Signs uses it |
|---|---|---|
| Computer Vision | Software that extracts information from images or video | Reads a reference video frame by frame to find hand and body points |
| MediaPipe | A library with ready-made models for detecting body, face and hand points | Supplies the hand and pose detection used by the POC/MVP |
| Landmark | One detected point, such as a wrist or fingertip | Stores where a joint appears in each frame |
| Skeleton | Lines connecting selected landmarks into a simple body/hand view | Makes structured movement visible for inspection |
| Movement representation | Movement stored as ordered data rather than only pixels | Keeps landmarks, timestamps and derived trajectories from the reference |
| Hand coverage | The share of video frames where the expected hand landmarks were detected | The versioned WATER reference has 93.98% dominant-hand coverage; this is not sign accuracy |
| Trajectory | The path a point follows over time | Measures how the wrist or fingertips move between frames |
| State machine | Rules defining which status changes are allowed | Allows Draft → Review → Approved → Published, but blocks Draft → Published |
| Deterministic rule | A normal code rule that gives the same answer for the same input | Checks required fields, banned claims and human-approval presence |
| Provenance | A record of where content and evidence came from | Links a sign version to its source, CV run, content, artwork and review |
| SHA-256 hash | A digital fingerprint calculated from a file or data | Detects whether referenced evidence or sign data changed |
| Audit log | An ordered record of important events | Records local content-operation events with synthetic actor types |
| Idempotency | Repeating the same operation does not create accidental duplicates or a different result | Rebuilding unchanged MORE inputs keeps the same package identity |
| Regression test | A repeatable check that detects when a change breaks existing behaviour | Reruns POC, MVP and content-operation cases after code changes |
| Golden set / evaluation set | A small stable group of examples used repeatedly | Uses MORE, EAT, WATER, ALL DONE and HELP for engineering readiness checks, not sign certification |
| n8n | A tool for connecting steps in a workflow | Routes structured content through preparation, checks and review output |
| Orchestration | Moving information through defined steps in the right order | Coordinates content work without giving the workflow approval authority |
| LLM | A language model that creates or edits text | Optionally drafts short family wording from supplied source content |
| LangSmith | A tool for recording and evaluating LLM runs | Shows what prompt/output would be traced for optional family-copy assistance |
| Human-in-the-loop | A person keeps control of a decision made after automated assistance | Requires human approval before publication |
| Publication package | A fixed set of versioned records for one release candidate | Binds source, technical evidence, content, visual and review state |
| SVG | A vector image format that remains sharp at different sizes | Intended format for controlled character and sign-specific hand assets |
| Retargeting | Applying captured movement to a different visual character or skeleton | A future avatar step; it has not been validated or implemented for production |
