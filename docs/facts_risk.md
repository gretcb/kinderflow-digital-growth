# Risk facts

This inventory supports later risk work. It is not a legal opinion or a claim that controls are production-ready.

| Risk | Why it matters | Current control | What is still unknown |
|---|---|---|---|
| Reference rights or sign identity are unclear | Unverified material cannot become a trusted commercial asset | MORE is marked `REVIEW_NEEDED`; the POC evidence scope is explicitly bounded | Who owns the source, what sign it represents and whether external use is permitted |
| Detection coverage is mistaken for sign correctness | A technical metric could create a false quality claim | POC/UI/docs say 93.98% is hand coverage and require human review | Whether every presentation surface preserves that distinction under sales pressure |
| Single-video technical evidence | One performer/capture condition cannot establish general performance | Current conclusion is “Proceed with conditions” | Behaviour across signs, performers, devices, lighting and viewpoints |
| Missing/abrupt landmark segments | Derived motion may be incomplete or noisy | Conservative interpolation, unresolved gaps and robust jump flags are reported | Effect on future retargeting and professional perception |
| Final visual changes the sign | A generic avatar or hand asset may alter important movement | Character and hand assets are separate; missing hand review blocks publication | Viable retargeting method and acceptable movement fidelity |
| Unsupported family claims | Families could receive misleading developmental or clinical wording | Deterministic banned-claim checks and human review | Reviewer consistency and performance on wider content |
| LLM drift or hallucination | Optional wording may add claims or movement detail | Grounded prompt, schema, gate, dry-run evaluation plan | Live model behaviour, prompt/version monitoring and failure rate |
| Automated workflow bypasses approval | Content could be published without accountability | State machine and n8n contract block autonomous publication | Enforcement in a real hosted workflow and reviewer permissions |
| Child/privacy scope expands | Child media or health data would sharply increase risk | Core flow requires no child video; pilot schema uses synthetic/pseudonymous IDs | Actual pilot data flow, vendors, retention, legal roles and notices |
| Local run artifacts persist | Reference video and derived data may remain longer than needed | Git ignores run/media artifacts; processing is local | Approved retention/deletion and access controls for production |
| Unauthenticated local approval UI | “Published” could be mistaken for a governed record | UI states say local/demo; content-ops package remains blocked | Production identity, authorisation, audit integrity and rollback |
| n8n import/runtime differences | A documented workflow may not execute unchanged | Credential-free export and node specification exist | Compatibility with the user’s installed n8n version and content-ops adapter run |
| Hosted MediaPipe runtime | Desktop graphics/runtime assumptions may fail in deployment | MVP documents the macOS graphics-context limitation | Container/runtime design, concurrency, performance and monitoring |
| Python environment is inconsistent | The default shell is Python 3.13, the documented target is 3.11/3.12, and the existing working `poc_env` reports 3.9.6 | MediaPipe 0.10.14 in `poc_env` passes the non-integration MVP tests | Rebuild and lock a supported 3.11/3.12 environment before hand-off |
| Browser print differences | Family assets may render differently across browsers/printers | Fixed templates and dedicated print CSS | Visual QA across target browsers, paper settings and grayscale printers |
| School/family adoption is weak | A technically working asset may not solve a paid problem | Future pilot metrics are defined | Actual use, effort, retention and willingness to pay |
| Operational review is too slow or costly | Human control is essential but may constrain the service | Review states and timestamps are modelled | Reviewer supply, SLA, rework and per-item cost |
| Illustrative prototype metrics are repeated as results | Static numbers could be mistaken for traction | UI labels them illustrative/static | Final presentation discipline and removal of ambiguous slides/screens |
