from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[2]
PROTOTYPE_ROOT = REPO_ROOT / "prototype"


def source(name: str) -> str:
    return (PROTOTYPE_ROOT / name).read_text(encoding="utf-8")


def compact(value: str) -> str:
    return " ".join(value.split())


class ContractNode:
    def __init__(
        self,
        tag: str,
        attrs: List[Tuple[str, Optional[str]]],
        parent: Optional["ContractNode"] = None,
    ) -> None:
        self.tag = tag
        self.attrs: Dict[str, str] = {
            key: value or "" for key, value in attrs
        }
        self.parent = parent
        self.children: List["ContractNode"] = []
        self.text: List[str] = []
        self.content: List[object] = []

    def descendants(self) -> List["ContractNode"]:
        output: List[ContractNode] = []
        for child in self.children:
            output.append(child)
            output.extend(child.descendants())
        return output

    def all_text(self) -> str:
        values = [
            item.all_text() if isinstance(item, ContractNode) else str(item)
            for item in self.content
        ]
        return compact(" ".join(values))

    def has_class(self, name: str) -> bool:
        return name in self.attrs.get("class", "").split()


class ContractTree(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__()
        self.root = ContractNode("document", [])
        self.stack = [self.root]

    def handle_starttag(
        self, tag: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        node = ContractNode(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        self.stack[-1].content.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(
        self, tag: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        node = ContractNode(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        self.stack[-1].content.append(node)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.stack[-1].text.append(data)
            self.stack[-1].content.append(data)

    def by_id(self, element_id: str) -> ContractNode:
        matches = [
            node
            for node in self.root.descendants()
            if node.attrs.get("id") == element_id
        ]
        if len(matches) != 1:
            raise AssertionError(
                "expected one #{0}, found {1}".format(element_id, len(matches))
            )
        return matches[0]

    def by_class(self, class_name: str) -> List[ContractNode]:
        return [
            node for node in self.root.descendants() if node.has_class(class_name)
        ]


def parse_html(name: str) -> ContractTree:
    tree = ContractTree()
    tree.feed(source(name))
    tree.close()
    return tree


def node_json(harness: str, *paths: Path) -> dict:
    node = shutil.which("node")
    if not node:
        raise unittest.SkipTest("Node is unavailable")
    result = subprocess.run(
        [node, "-e", harness, *[str(path) for path in paths]],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise AssertionError("Node harness returned invalid JSON: " + result.stdout) from error


CREATE_SIGN_HARNESS = r'''
const fs = require("fs");
const vm = require("vm");

let sequence = 0;
const registry = new Map();
class Element {
  constructor(key, tagName = "div") {
    this.key = key;
    this.tagName = tagName.toLowerCase();
    this.children = [];
    this.listeners = {};
    this.attributes = {};
    this.dataset = {};
    this.style = {};
    this.textContent = "";
    this.className = "";
    this.value = "";
    this.href = "";
    this.src = "";
    this.hidden = false;
    this.disabled = false;
    this.checked = false;
    this.complete = true;
    this.naturalWidth = 100;
    this.classList = {
      add: (...names) => {
        const values = new Set(this.className.split(/\s+/).filter(Boolean));
        names.forEach((name) => values.add(name));
        this.className = [...values].join(" ");
      },
      remove: (...names) => {
        const remove = new Set(names);
        this.className = this.className.split(/\s+/).filter((name) => name && !remove.has(name)).join(" ");
      },
      toggle: (name, force) => {
        const active = this.className.split(/\s+/).includes(name);
        if (force === true || (!active && force !== false)) this.classList.add(name);
        else if (active) this.classList.remove(name);
      }
    };
  }
  addEventListener(type, listener) { (this.listeners[type] ||= []).push(listener); }
  dispatch(type) {
    if (type === "click" && this.disabled) return;
    const event = { currentTarget: this, target: this, preventDefault() {} };
    for (const listener of this.listeners[type] || []) listener(event);
  }
  append(...children) {
    for (const child of children) {
      if (child && typeof child === "object") child.parent = this;
      this.children.push(child);
    }
  }
  prepend(...children) { this.children.unshift(...children); }
  replaceChildren(...children) {
    this.children = [];
    this.append(...children);
  }
  walk() {
    const output = [];
    for (const child of this.children) {
      if (!child || typeof child !== "object") continue;
      output.push(child);
      output.push(...child.walk());
    }
    return output;
  }
  querySelector(selector) { return element(`${this.key} ${selector}`); }
  querySelectorAll(selector) {
    if (selector === "input:checked") {
      return this.walk().filter((item) => item.tagName === "input" && item.checked);
    }
    if (selector === 'input[type="checkbox"]') {
      return this.walk().filter((item) => item.tagName === "input" && item.type === "checkbox");
    }
    return [];
  }
  setAttribute(name, value) {
    this.attributes[name] = String(value);
    if (name === "src") this.src = String(value);
    if (name === "href") this.href = String(value);
  }
  getAttribute(name) { return this.attributes[name] ?? null; }
  removeAttribute(name) {
    delete this.attributes[name];
    if (name === "src") this.src = "";
    if (name === "href") this.href = "";
  }
  pause() { this.pauseCount = (this.pauseCount || 0) + 1; }
  load() {}
  focus() { this.focused = true; }
  scrollIntoView() {}
  remove() { this.removed = true; }
  decode() { return Promise.resolve(); }
  closest() { return null; }
}
const element = (selector) => {
  if (!registry.has(selector)) registry.set(selector, new Element(selector));
  return registry.get(selector);
};
const evidenceInputs = [
  Object.assign(new Element("tracked", "input"), { value: "LANDMARK_KEY_POSE" }),
  Object.assign(new Element("frames", "input"), { value: "HUMAN_SELECTED_FRAME" }),
  Object.assign(new Element("reviewed", "input"), { value: "KNOWLEDGE_REFERENCE_FALLBACK" })
];
const referenceModeInputs = [
  Object.assign(new Element("input-upload", "input"), { value: "upload", checked: true }),
  Object.assign(new Element("input-url", "input"), { value: "url" })
];
const storage = new Map();
const document = {
  querySelector: element,
  querySelectorAll(selector) {
    if (selector === 'input[name="evidence_route"]') return evidenceInputs;
    if (selector === 'input[name="reference_input_mode"]') return referenceModeInputs;
    if (selector === 'input[name="visual_candidate"]') return [];
    if (selector === "[data-active-sign]") return [element("[data-active-sign]")];
    if (selector === ".visual-candidate-card") return [];
    return [];
  },
  createElement(tagName) { return new Element(`created-${tagName}-${++sequence}`, tagName); },
  fonts: { ready: Promise.resolve() }
};
const windowObject = {
  setTimeout: () => 1,
  clearTimeout() {},
  location: { search: "", assign() {} }
};
let fetchCount = 0;
const context = {
  document,
  window: windowObject,
  sessionStorage: {
    setItem(key, value) { storage.set(key, String(value)); },
    getItem(key) { return storage.has(key) ? storage.get(key) : null; },
    removeItem(key) { storage.delete(key); }
  },
  fetch: () => { fetchCount += 1; return new Promise(() => {}); },
  FormData: class { append() {} },
  URL,
  URLSearchParams,
  encodeURIComponent,
  console
};
vm.createContext(context);
const script = fs.readFileSync(process.argv[1], "utf8");
vm.runInContext(script + `
;globalThis.__contract = {
  state,
  finishRun,
  updateEvidenceRouteUi,
  renderSuggestedFrames,
  trackedPosesAreAvailable,
  restoreWorkflowFromSession,
  syncReferenceInputMode,
  renderIllustrativeVideo,
  clearReference
};`, context);

const contract = context.__contract;
const candidate = {
  id: "more-b",
  asset: "assets/signs/more-b.svg",
  content_hash: "test-hash",
  title: "Clear movement sequence",
  review_note: "Review the hands",
  recommended: true
};
const signPackage = {
  sign_id: "more",
  labels: { en: "MORE", es: "MÁS" },
  candidates: [candidate],
  regeneration_candidates: [],
  review_status: "READY_FOR_HUMAN_REVIEW",
  evidence_routes: {
    pass: "LANDMARK_KEY_POSE",
    review: "HUMAN_SELECTED_FRAME",
    fallback: "KNOWLEDGE_REFERENCE_FALLBACK"
  },
  grounding_sources: [{ status: "Applied" }],
  movement: {
    hands: 2,
    body_location: "Upper chest",
    description: "Bring both hands together.",
    presentation: "Show the repeated movement."
  },
  knowledge: {
    direction: "Inward",
    hands_used: 2,
    body_location: "Upper chest",
    expected_key_pose_count: 2
  }
};
contract.state.visualPackages = [signPackage];
contract.state.illustrativeCatalog = {
  more: {
    sign_id: "more",
    label: "MORE",
    available: true,
    url: "/api/illustrative-videos/more",
    provider: "Google Labs FX / Gemini FX",
    usage_status: "GOOGLE_LABS_FX_OUTPUT_USAGE_CONFIRMATION_NEEDED"
  },
  water: { sign_id: "water", label: "WATER", available: false, url: null }
};
referenceModeInputs[1].dispatch("change");
element("#direct-video-url").value = "https://example.com/more.mp4";
element("#direct-video-url").dispatch("input");
const urlMode = {
  source: contract.state.source,
  inputMode: contract.state.inputMode,
  uploadHidden: element("#upload-source-panel").hidden,
  uploadDisabled: element("#reference-video").disabled,
  urlHidden: element("#url-source-panel").hidden,
  urlDisabled: element("#direct-video-url").disabled,
  runDisabled: element("#run-movement-check").disabled
};
element("#use-demo-video").dispatch("click");
const demoShortcut = {
  source: contract.state.source,
  inputMode: contract.state.inputMode,
  sign: element("#sign-name").value,
  signDisabled: element("#sign-name").disabled,
  directUrl: element("#direct-video-url").value,
  uploadHidden: element("#upload-source-panel").hidden,
  urlHidden: element("#url-source-panel").hidden
};
contract.syncReferenceInputMode("upload");
const frames = ["a", "b", "c"].map((id, index) => ({
  id: `pose-${id}`,
  label: `Pose ${String.fromCharCode(65 + index)}`,
  url: `/runs/test/pose-${id}.jpg`
}));
const makeRun = (technicalStatus) => ({
  run_id: `run_${technicalStatus.replaceAll(" ", "_")}`,
  state: "complete",
  sign: { sign_id: "more", name: "MORE", routine_context: "Playtime" },
  source: {},
  technical_status: technicalStatus,
  metrics: {
    frames_analysed: 100,
    pose_detection_coverage_percent: 100,
    dominant_hand_detection_coverage_percent: technicalStatus === "Pass" ? 90 : 89.99,
    missing_hand_frames: technicalStatus === "Pass" ? 10 : 11,
    unresolved_frames: 4,
    unresolved_frames_percent: 4
  },
  warnings: ["4 unresolved frames (4.0%) remain."],
  technical_details: {},
  artifacts: {
    suggested_reference_frames: frames,
    reference_video_url: "/runs/test/input/reference.mp4",
    movement_preview_url: "/runs/test/output/reference_landmarks.mp4",
    detection_timeline_url: "/runs/test/output/detection.png",
    wrist_trajectory_url: "/runs/test/output/wrist.png"
  },
  processing: { duration_seconds: 1.2 }
});

const finish = (technicalStatus) => {
  const run = makeRun(technicalStatus);
  contract.state.run = run;
  contract.finishRun(run);
};

finish("Review needed");
const frameContainer = element("#suggested-reference-frames");
const frameInputs = frameContainer.walk().filter((item) => item.tagName === "input");
const primarySelectors = [
  "#result-kicker", "#result-title", "#result-explanation", "#technical-status",
  "#review-title", "#review-guidance", "#review-state", "#review-message"
];
const review = {
  resultTitle: element("#result-title").textContent,
  explanation: element("#result-explanation").textContent,
  badge: element("#review-state").textContent,
  warningCount: primarySelectors.filter((selector) => element(selector).textContent === "Review recommended").length,
  trackedDisabled: evidenceInputs[0].disabled,
  trackedHelpHidden: element("#tracked-pose-availability").hidden,
  action: element("#approve-sign").textContent,
  actionDisabled: element("#approve-sign").disabled,
  secondary: element("#use-another-reference").textContent,
  help: element("#frame-picker-help").textContent
};

frameInputs[0].checked = true;
frameInputs[0].dispatch("change");
const one = {
  help: element("#frame-picker-help").textContent,
  disabled: element("#approve-sign").disabled,
  selected: [...contract.state.selectedFrames]
};
frameInputs[1].checked = true;
frameInputs[1].dispatch("change");
const two = {
  help: element("#frame-picker-help").textContent,
  disabled: element("#approve-sign").disabled,
  selected: [...contract.state.selectedFrames]
};
frameInputs[2].checked = true;
frameInputs[2].dispatch("change");
const max = {
  thirdChecked: frameInputs[2].checked,
  selected: [...contract.state.selectedFrames]
};

element("#approve-sign").dispatch("click");
contract.state.selectedCandidate = candidate;
element("#approve-visual").disabled = false;
element("#approve-visual").dispatch("click");
const workflow = JSON.parse(storage.get("kinderflowVisualWorkflow"));
const approvedVisual = JSON.parse(storage.get("kinderflowApprovedVisual"));
const decisionLocks = {
  routes: evidenceInputs.map((input) => input.disabled),
  frames: frameInputs.map((input) => input.disabled),
  rationale: element("#technical-review-rationale").disabled
};
const workflowBeforeLockedMutation = storage.get("kinderflowVisualWorkflow");
const approvedBeforeLockedMutation = storage.get("kinderflowApprovedVisual");
evidenceInputs[2].checked = true;
evidenceInputs[2].dispatch("change");
frameInputs[0].checked = false;
frameInputs[0].dispatch("change");
const lockedMutation = {
  route: contract.state.evidenceRoute,
  selected: [...contract.state.selectedFrames],
  workflowUnchanged: storage.get("kinderflowVisualWorkflow") === workflowBeforeLockedMutation,
  approvalUnchanged: storage.get("kinderflowApprovedVisual") === approvedBeforeLockedMutation
};
const preparation = {
  titleSign: element("[data-active-sign]").textContent,
  reviewed: element("#grounding-source").textContent,
  reviewedStatus: element("#grounding-source-status").textContent,
  poses: element("#grounding-motion").textContent,
  posesStatus: element("#grounding-motion-status").textContent,
  illustration: element("#grounding-character").textContent,
  illustrationStatus: element("#grounding-character-status").textContent,
  routine: element("#visual-routine-context").textContent,
  printableHref: element("#create-printable-link").href
};

const completedRunId = contract.state.run.run_id;
const evidenceBeforePoseReset = {
  fetchCount,
  referenceVideo: element("#reference-video-preview").src,
  movementVideo: element("#movement-video-preview").src,
  timeline: element("#detection-timeline").src,
  wrist: element("#wrist-trajectory").src,
  frames: element("#metric-frames").textContent,
  hand: element("#metric-hand").textContent,
  storedRun: JSON.parse(storage.get("kinderflowReferenceReview")).run_id,
  illustrativeSrc: element("#illustrative-video").src,
  illustrativeAvailable: !element("#illustrative-video-available").hidden
};
element("#choose-different-evidence").dispatch("click");
const poseReset = {
  runId: contract.state.run.run_id,
  reviewTitle: element("#review-title").textContent,
  reviewMessage: element("#review-message").textContent,
  visualHidden: element("#visual-review-section").hidden,
  familyHidden: element("#downstream-section").hidden,
  workflow: JSON.parse(storage.get("kinderflowVisualWorkflow")),
  approvedVisual: storage.get("kinderflowApprovedVisual") || null,
  routesUnlocked: evidenceInputs.some((input) => !input.disabled),
  framesUnlocked: frameInputs.every((input) => !input.disabled),
  rationaleUnlocked: !element("#technical-review-rationale").disabled,
  fetchCount,
  resultVisible: !element("#result-section").hidden,
  reviewVisible: !element("#review-section").hidden,
  referenceVideo: element("#reference-video-preview").src,
  movementVideo: element("#movement-video-preview").src,
  timeline: element("#detection-timeline").src,
  wrist: element("#wrist-trajectory").src,
  frames: element("#metric-frames").textContent,
  hand: element("#metric-hand").textContent,
  storedRun: JSON.parse(storage.get("kinderflowReferenceReview")).run_id,
  illustrativeHidden: element("#illustrative-motion-section").hidden,
  illustrativeSrc: element("#illustrative-video").src
};
contract.state.activePackage = { ...signPackage, sign_id: "water" };
element("#visual-preparation-section").hidden = false;
contract.renderIllustrativeVideo();
const missingIllustrative = {
  videoSrc: element("#illustrative-video").src,
  availableHidden: element("#illustrative-video-available").hidden,
  missingVisible: !element("#illustrative-video-missing").hidden,
  disclosureHidden: element("#illustrative-primary-disclosure").hidden,
  technicalHidden: element("#illustrative-technical-details").hidden,
  visualPreparationStillAvailable: !element("#visual-preparation-section").hidden
};
contract.state.activePackage = signPackage;

finish("Pass");
const pass = {
  trackedDisabled: evidenceInputs[0].disabled,
  trackedHelpHidden: element("#tracked-pose-availability").hidden,
  actionDisabled: element("#approve-sign").disabled
};

const threshold = {
  missing: contract.trackedPosesAreAvailable({ metrics: {} }),
  below: contract.trackedPosesAreAvailable({ metrics: { dominant_hand_detection_coverage_percent: 89.99 } }),
  exact: contract.trackedPosesAreAvailable({ metrics: { dominant_hand_detection_coverage_percent: 90 } }),
  above: contract.trackedPosesAreAvailable({ metrics: { dominant_hand_detection_coverage_percent: 99.5 } })
};
finish("Unknown");
const unknownStatus = {
  actionHidden: element("#approve-sign").hidden,
  candidates: contract.state.currentCandidates.length,
  reviewTitle: element("#review-title").textContent
};
const missingStatusRun = makeRun("Review needed");
delete missingStatusRun.technical_status;
contract.state.run = missingStatusRun;
contract.finishRun(missingStatusRun);
const missingStatus = {
  actionHidden: element("#approve-sign").hidden,
  candidates: contract.state.currentCandidates.length
};

const restoreRun = makeRun("Review needed");
windowObject.location.search = `?restore=1&run=${encodeURIComponent(restoreRun.run_id)}`;
storage.set("kinderflowReferenceReview", JSON.stringify(restoreRun));

(async () => {
  contract.state.visualPackages = [];
  storage.set("kinderflowVisualWorkflow", JSON.stringify(workflow));
  storage.set("kinderflowApprovedVisual", JSON.stringify(approvedVisual));
  element("#downstream-section").hidden = true;
  await contract.restoreWorkflowFromSession();
  const missingPackageRestore = {
    downstreamHidden: element("#downstream-section").hidden,
    activePackage: contract.state.activePackage
  };
  contract.state.visualPackages = [signPackage];

  storage.set("kinderflowVisualWorkflow", JSON.stringify({
    ...workflow,
    technical_review_action: "REJECT"
  }));
  storage.set("kinderflowApprovedVisual", JSON.stringify(approvedVisual));
  contract.state.selectedCandidate = null;
  element("#downstream-section").hidden = true;
  await contract.restoreWorkflowFromSession();
  const wrongActionRestore = {
    downstreamHidden: element("#downstream-section").hidden,
    selectedCandidate: contract.state.selectedCandidate?.id || null,
    action: JSON.parse(storage.get("kinderflowVisualWorkflow")).technical_review_action,
    approval: storage.get("kinderflowApprovedVisual") || null
  };

  storage.set("kinderflowVisualWorkflow", JSON.stringify({
    ...workflow,
    selected_reference_frames: []
  }));
  storage.set("kinderflowApprovedVisual", JSON.stringify(approvedVisual));
  element("#downstream-section").hidden = true;
  await contract.restoreWorkflowFromSession();
  const zeroFrameRestore = {
    action: JSON.parse(storage.get("kinderflowVisualWorkflow")).technical_review_action,
    selected: [...contract.state.selectedFrames],
    approval: storage.get("kinderflowApprovedVisual") || null,
    approveDisabled: element("#approve-sign").disabled
  };

  storage.set("kinderflowVisualWorkflow", JSON.stringify({
    ...workflow,
    selected_reference_frames: frames.map((frame) => frame.id)
  }));
  storage.set("kinderflowApprovedVisual", JSON.stringify(approvedVisual));
  element("#downstream-section").hidden = true;
  await contract.restoreWorkflowFromSession();
  const threeFrameRestore = {
    action: JSON.parse(storage.get("kinderflowVisualWorkflow")).technical_review_action,
    selected: [...contract.state.selectedFrames],
    approval: storage.get("kinderflowApprovedVisual") || null,
    approveDisabled: element("#approve-sign").disabled
  };

  storage.set("kinderflowVisualWorkflow", JSON.stringify({
    ...workflow,
    visual_review_status: "REJECTED",
    internal_printable_eligible: false
  }));
  storage.set("kinderflowApprovedVisual", JSON.stringify({
    ...approvedVisual,
    status: "REJECTED",
    internal_printable_eligible: false
  }));
  element("#downstream-section").hidden = true;
  await contract.restoreWorkflowFromSession();
  const rejectedRestore = {
    downstreamHidden: element("#downstream-section").hidden,
    selectedCandidate: contract.state.selectedCandidate?.id || null
  };

  storage.set("kinderflowVisualWorkflow", JSON.stringify(workflow));
  storage.set("kinderflowApprovedVisual", JSON.stringify(approvedVisual));
  element("#downstream-section").hidden = true;
  await contract.restoreWorkflowFromSession();
  const approvedRestore = {
    downstreamHidden: element("#downstream-section").hidden,
    selectedCandidate: contract.state.selectedCandidate?.id || null,
    runId: contract.state.run?.run_id || null
  };
  const previewBeforeFullReset = {
    src: element("#illustrative-video").src,
    pauseCount: element("#illustrative-video").pauseCount || 0
  };
  element("#reset-sign-run").dispatch("click");
  const fullReset = {
    rationaleDisabled: element("#technical-review-rationale").disabled,
    referenceReview: storage.get("kinderflowReferenceReview") || null,
    workflow: storage.get("kinderflowVisualWorkflow") || null,
    approval: storage.get("kinderflowApprovedVisual") || null,
    illustrativeSrc: element("#illustrative-video").src,
    illustrativePaused: (element("#illustrative-video").pauseCount || 0) > previewBeforeFullReset.pauseCount
  };

  element("#sign-name").value = "HELP";
  element("#routine-context").value = "Playtime";
  referenceModeInputs[1].dispatch("change");
  element("#direct-video-url").value = "https://example.com/help.mp4";
  element("#direct-video-url").dispatch("input");
  const fetchesBeforeSubmit = fetchCount;
  element("#sign-run-form").dispatch("submit");
  element("#sign-run-form").dispatch("submit");
  referenceModeInputs[0].dispatch("change");
  element("#use-demo-video").dispatch("click");
  const inFlightGuard = {
    fetchDelta: fetchCount - fetchesBeforeSubmit,
    pending: contract.state.submissionPending,
    source: contract.state.source,
    inputMode: contract.state.inputMode,
    sign: element("#sign-name").value,
    modeControlsLocked: referenceModeInputs.every((input) => input.disabled),
    signLocked: element("#sign-name").disabled,
    routineLocked: element("#routine-context").disabled,
    urlLocked: element("#direct-video-url").disabled,
    demoLocked: element("#use-demo-video").disabled
  };

  process.stdout.write(JSON.stringify({ urlMode, demoShortcut, review, one, two, max, preparation, workflow, approvedVisual, decisionLocks, lockedMutation, completedRunId, evidenceBeforePoseReset, poseReset, missingIllustrative, pass, threshold, unknownStatus, missingStatus, missingPackageRestore, wrongActionRestore, zeroFrameRestore, threeFrameRestore, rejectedRestore, approvedRestore, fullReset, inFlightGuard }));
})().catch((error) => {
  process.stderr.write(error.stack || String(error));
  process.exitCode = 1;
});
'''


FLASHCARD_HARNESS = r'''
const fs = require("fs");
const vm = require("vm");

let sequence = 0;
const registry = new Map();
class Element {
  constructor(key, tagName = "div") {
    this.key = key;
    this.tagName = tagName;
    this.children = [];
    this.listeners = {};
    this.attributes = {};
    this.dataset = {};
    this.textContent = "";
    this.className = "";
    this.value = "";
    this.href = "";
    this.src = "";
    this.alt = "";
    this.hidden = false;
    this.disabled = false;
    this.checked = false;
    this.complete = true;
    this.naturalWidth = 100;
    this.classList = { add() {}, remove() {}, toggle() {} };
  }
  addEventListener(type, listener) { (this.listeners[type] ||= []).push(listener); }
  dispatch(type) {
    if (type === "click" && this.disabled) return;
    const event = { currentTarget: this, target: this, preventDefault() {} };
    for (const listener of this.listeners[type] || []) listener(event);
  }
  append(...children) { this.children.push(...children); }
  prepend(...children) { this.children.unshift(...children); }
  replaceChildren(...children) { this.children = children; }
  querySelector(selector) { return element(`${this.key} ${selector}`); }
  querySelectorAll() { return []; }
  setAttribute(name, value) {
    this.attributes[name] = String(value);
    if (name === "href") this.href = String(value);
    if (name === "src") this.src = String(value);
  }
  getAttribute(name) { return this.attributes[name] ?? null; }
  removeAttribute(name) {
    delete this.attributes[name];
    if (name === "src") this.src = "";
  }
  focus() { this.focused = true; }
  decode() { return Promise.resolve(); }
}
const element = (selector) => {
  if (!registry.has(selector)) registry.set(selector, new Element(selector));
  return registry.get(selector);
};
const languageInputs = [
  Object.assign(new Element("language-en", "input"), { value: "en", checked: true }),
  Object.assign(new Element("language-es", "input"), { value: "es" })
];
const cardInputs = [
  Object.assign(new Element("card-flashcard", "input"), { value: "flashcard", checked: true }),
  Object.assign(new Element("card-routine", "input"), { value: "routine" })
];
const document = {
  querySelector(selector) {
    const language = selector.match(/^input\[name="language"\](?:\[value="([^"]+)"\])?(?::checked)?$/);
    if (language) return language[1]
      ? languageInputs.find((input) => input.value === language[1])
      : languageInputs.find((input) => input.checked);
    const cardType = selector.match(/^input\[name="card_type"\](?:\[value="([^"]+)"\])?(?::checked)?$/);
    if (cardType) return cardType[1]
      ? cardInputs.find((input) => input.value === cardType[1])
      : cardInputs.find((input) => input.checked);
    return element(selector);
  },
  querySelectorAll(selector) {
    if (selector === 'input[name="language"]') return languageInputs;
    if (selector === 'input[name="card_type"]') return cardInputs;
    return [];
  },
  createElement(tagName) { return new Element(`created-${tagName}-${++sequence}`, tagName); }
};
const storage = new Map();
let assignedLocation = "";
let assetLoadMode = "ready";
const windowObject = {
  location: {
    search: "?sign=more&visual=more-b&approved=1&restore=1&type=routine&lang=es&routine=Playtime",
    assign(value) { assignedLocation = value; }
  },
  print() {}
};
const context = {
  document,
  window: windowObject,
  sessionStorage: {
    setItem(key, value) { storage.set(key, String(value)); },
    getItem(key) { return storage.has(key) ? storage.get(key) : null; },
    removeItem(key) { storage.delete(key); }
  },
  fetch: (url) => {
    if (String(url).endsWith(".svg")) {
      if (assetLoadMode === "pending") return new Promise(() => {});
      return Promise.resolve({ ok: false, text: async () => "" });
    }
    return new Promise(() => {});
  },
  URLSearchParams,
  Option: class extends Element {
    constructor(text, value) { super("option", "option"); this.textContent = text; this.value = value; }
  },
  DOMParser: class {},
  XMLSerializer: class {},
  encodeURIComponent,
  console
};
vm.createContext(context);
const script = fs.readFileSync(process.argv[1], "utf8");
vm.runInContext(script + `
;globalThis.__contract = {
  builder,
  render,
  localizeRoutineContext,
  normalizeRoutineContext,
  loadApprovedVisual,
  loadPrintableApproval,
  approvedCandidateFor,
  restorePrintableReady,
  outputFor
};`, context);
const contract = context.__contract;
const candidate = {
  id: "more-b",
  asset: "assets/signs/more-b.svg",
  content_hash: "hash-more-b",
  title: "Clear movement sequence"
};
const sign = {
  id: "sign-more",
  sign_id: "more",
  display_name: "MORE",
  spanish_label: "MÁS",
  routine: { en: "Snack time", es: "Hora de la merienda" },
  short_family_guidance: {
    en: "Use the sign naturally during the routine.",
    es: "Usa el signo de forma natural durante la rutina."
  },
  printable: true
};
const signPackage = {
  sign_id: "more",
  candidates: [candidate],
  regeneration_candidates: [],
  contextual_image: null,
  routine: sign.routine,
  movement: { presentation: "MEET · SEPARATE · REPEAT" }
};
const approvedVisual = {
  sign_id: "more",
  candidate_id: candidate.id,
  asset: candidate.asset,
  content_hash: candidate.content_hash,
  routine_context: "Playtime",
  cv_run_id: "run_more",
  status: "APPROVED_FOR_INTERNAL_PRINTABLE",
  internal_printable_eligible: true,
  publication_status: "DRAFT"
};
const printableApproval = {
  sign_id: "more",
  candidate_id: candidate.id,
  asset: candidate.asset,
  content_hash: candidate.content_hash,
  card_type: "routine",
  language: "es",
  routine_context: { en: "Playtime", es: "Hora de jugar" },
  family_guidance: {
    en: "Approved guidance snapshot.",
    es: "Guía aprobada."
  },
  status: "PRINTABLE_READY",
  publication_status: "DRAFT"
};
const workflow = {
  sign_id: "more",
  cv_run_id: "run_more",
  selected_candidate_id: candidate.id,
  visual_review_status: "APPROVED_FOR_INTERNAL_PRINTABLE",
  internal_printable_eligible: true,
  publication_status: "DRAFT"
};
storage.set("kinderflowApprovedVisual", JSON.stringify(approvedVisual));
storage.set("kinderflowPrintableApproval", JSON.stringify(printableApproval));
storage.set("kinderflowVisualWorkflow", JSON.stringify(workflow));
Object.assign(contract.builder, {
  signs: [sign],
  selectedId: sign.id,
  language: "es",
  cardType: "routine",
  visualPackages: [signPackage],
  approvedVisual: contract.loadApprovedVisual(),
  printableApproval: contract.loadPrintableApproval(),
  requestedRoutine: "Playtime",
  requestedSignId: "more"
});
languageInputs.forEach((input) => { input.checked = input.value === "es"; });
cardInputs.forEach((input) => { input.checked = input.value === "routine"; });
(async () => {
contract.render();
await new Promise((resolve) => setImmediate(resolve));

const card = element(".flashcard-output");
const inner = (selector) => element(`.flashcard-output ${selector}`);
const visibleText = (item) => [
  item.textContent,
  ...item.children.map((child) => typeof child === "string" ? child : child.textContent)
].join("").trim();
const spanish = {
  word: inner("[data-card-sign]").textContent,
  secondaryHidden: inner("[data-card-spanish]").hidden,
  kind: inner("[data-card-kind]").textContent,
  routineLabel: inner('[data-card-label="routine"]').textContent,
  routine: inner("[data-card-routine]").textContent,
  guidanceLabel: inner('[data-card-label="guidance"]').textContent,
  guidance: inner("[data-card-guidance]").textContent,
  movement: visibleText(inner("[data-movement-caption]")),
  iconLabel: inner("[data-routine-icon]").attributes["aria-label"],
  ready: contract.builder.layoutReviewed,
  readyText: element("#review-state-text").textContent,
  printText: element("#print-flashcard").textContent,
  postActionsHidden: element("#post-approval-actions").hidden
};
element("#print-flashcard").dispatch("click");
const printHref = assignedLocation;
const beforeAnother = {
  selectedId: contract.builder.selectedId,
  candidateId: contract.builder.approvedVisual.candidate_id,
  asset: contract.builder.approvedVisual.asset
};
element("#create-another").dispatch("click");
const afterAnother = {
  selectedId: contract.builder.selectedId,
  candidateId: contract.builder.approvedVisual.candidate_id,
  asset: contract.builder.approvedVisual.asset,
  printableApproval: contract.builder.printableApproval
};

contract.builder.language = "en";
contract.builder.cardType = "flashcard";
contract.builder.requestedRoutine = null;
contract.builder.printableApproval = null;
contract.builder.approvedVisual = { ...approvedVisual, routine_context: "Garden tidy-up" };
contract.render();
await new Promise((resolve) => setImmediate(resolve));
const contextImage = inner("[data-context-image]");
const contextPlaceholder = inner("[data-context-placeholder]");
const custom = {
  routine: inner("[data-card-routine]").textContent,
  cardVisible: !card.hidden,
  contextImageHidden: contextImage.hidden,
  contextImageSrc: contextImage.src,
  placeholderHidden: contextPlaceholder.hidden,
  placeholderText: contextPlaceholder.querySelector("strong").textContent,
  signImageSrc: inner("[data-sign-illustration]").src,
  signImageSourceAsset: inner("[data-sign-illustration]").dataset.sourceAsset
};
element("#review-flashcard").dispatch("click");
const savedPrintable = JSON.parse(storage.get("kinderflowPrintableApproval"));

const translations = {
  snack: contract.localizeRoutineContext("Snack time"),
  play: contract.localizeRoutineContext("Playtime"),
  meal: contract.localizeRoutineContext("Mealtime"),
  custom: contract.localizeRoutineContext("Garden tidy-up"),
  mixed: contract.localizeRoutineContext("Snack time / Garden tidy-up")
};
const originalVisual = JSON.stringify(approvedVisual);
const originalWorkflow = JSON.stringify(workflow);
const visualTrustCase = (visualUpdate = {}, workflowUpdate = {}) => {
  storage.set("kinderflowApprovedVisual", JSON.stringify({ ...approvedVisual, ...visualUpdate }));
  storage.set("kinderflowVisualWorkflow", JSON.stringify({ ...workflow, ...workflowUpdate }));
  const loaded = contract.loadApprovedVisual();
  contract.builder.approvedVisual = loaded;
  return { loaded: Boolean(loaded), candidate: Boolean(contract.approvedCandidateFor(sign)) };
};
storage.delete("kinderflowVisualWorkflow");
const missingWorkflow = Boolean(contract.loadApprovedVisual());
storage.set("kinderflowApprovedVisual", originalVisual);
storage.set("kinderflowVisualWorkflow", originalWorkflow);
const wrongWorkflowCandidate = visualTrustCase({}, { selected_candidate_id: "more-a" });
const wrongVisualHash = visualTrustCase({ content_hash: "tampered-hash" });
const wrongWorkflowPublication = visualTrustCase({}, { publication_status: "PUBLISHED" });
storage.set("kinderflowApprovedVisual", originalVisual);
storage.set("kinderflowVisualWorkflow", originalWorkflow);
contract.builder.approvedVisual = contract.loadApprovedVisual();
contract.builder.language = "es";
contract.builder.cardType = "routine";
const printableTrust = {
  wrongCandidate: (() => { contract.builder.printableApproval = { ...printableApproval, candidate_id: "more-a" }; return contract.restorePrintableReady(sign, candidate); })(),
  wrongType: (() => { contract.builder.printableApproval = { ...printableApproval, card_type: "flashcard" }; return contract.restorePrintableReady(sign, candidate); })(),
  wrongLanguage: (() => { contract.builder.printableApproval = { ...printableApproval, language: "en" }; return contract.restorePrintableReady(sign, candidate); })()
};
const trust = { missingWorkflow, wrongWorkflowCandidate, wrongVisualHash, wrongWorkflowPublication, printableTrust };
contract.builder.approvedVisual = contract.loadApprovedVisual();
contract.builder.printableApproval = {
  ...printableApproval,
  candidate_id: "more-a",
  routine_context: { en: "Stale routine", es: "Rutina obsoleta" },
  family_guidance: { en: "Stale guidance", es: "Orientación obsoleta" }
};
contract.builder.language = "en";
contract.builder.cardType = "routine";
const stalePrintableOutput = contract.outputFor(sign, candidate);
contract.builder.language = "es";
contract.builder.cardType = "flashcard";
contract.builder.printableApproval = null;
contract.builder.approvedVisual = contract.loadApprovedVisual();
signPackage.contextual_image = { asset: "assets/context/example.png", alt: "English-only context description" };
contract.render();
await new Promise((resolve) => setImmediate(resolve));
const spanishAccessibility = {
  signAlt: inner("[data-sign-illustration]").alt,
  contextAlt: inner("[data-context-image]").alt
};
assetLoadMode = "pending";
contract.builder.language = "en";
contract.builder.cardType = "flashcard";
contract.builder.printableApproval = null;
context.sessionStorage.removeItem("kinderflowPrintableApproval");
contract.render();
const pendingAsset = {
  approveDisabled: element("#review-flashcard").disabled,
  printableBeforeClick: storage.get("kinderflowPrintableApproval") || null
};
element("#review-flashcard").dispatch("click");
pendingAsset.printableAfterClick = storage.get("kinderflowPrintableApproval") || null;
process.stdout.write(JSON.stringify({ spanish, printHref, beforeAnother, afterAnother, custom, savedPrintable, translations, trust, stalePrintableOutput, spanishAccessibility, pendingAsset }));
})().catch((error) => {
  process.stderr.write(error.stack || String(error));
  process.exitCode = 1;
});
'''


PRINT_CARD_HARNESS = r'''
const fs = require("fs");
const vm = require("vm");

(async () => {
  const registry = new Map();
  class Element {
    constructor(key) {
      this.key = key;
      this.children = [];
      this.listeners = {};
      this.attributes = {};
      this.dataset = {};
      this.textContent = "";
      this.href = "";
      this.src = "";
      this.alt = "";
      this.hidden = false;
      this.disabled = false;
      this.complete = true;
      this.naturalWidth = 100;
    }
    addEventListener(type, listener) { (this.listeners[type] ||= []).push(listener); }
    querySelector(selector) { return element(`${this.key} ${selector}`); }
    querySelectorAll() { return []; }
    setAttribute(name, value) {
      this.attributes[name] = String(value);
      if (name === "href") this.href = String(value);
      if (name === "src") this.src = String(value);
    }
    removeAttribute(name) {
      delete this.attributes[name];
      if (name === "src") this.src = "";
    }
    remove() { this.removed = true; }
    decode() { return Promise.resolve(); }
  }
  const element = (selector) => {
    if (!registry.has(selector)) registry.set(selector, new Element(selector));
    return registry.get(selector);
  };
  const document = {
    querySelector: element,
    fonts: { ready: Promise.resolve() }
  };
  const card = element("#a5-print-card");
  card.hidden = true;
  element("#print-card-error").hidden = true;
  element("#open-print-dialog").disabled = true;

  const signsPayload = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const packagesPayload = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
  const helpPackage = packagesPayload.signs.find((item) => item.sign_id === "help");
  const helpCandidate = helpPackage.candidates[0];
  const morePackage = packagesPayload.signs.find((item) => item.sign_id === "more");
  const moreCandidate = morePackage.candidates.find((item) => item.id === "more-b") || morePackage.candidates[0];
  const approval = {
    sign_id: "help",
    candidate_id: helpCandidate.id,
    asset: helpCandidate.asset,
    content_hash: helpCandidate.content_hash,
    card_type: "flashcard",
    language: "en",
    routine_context: { en: "Garden tidy-up", es: "Garden tidy-up" },
    family_guidance: { en: "Approved guidance snapshot.", es: "Guía aprobada." },
    status: "PRINTABLE_READY",
    publication_status: "DRAFT"
  };
  const approvedVisual = {
    sign_id: "help",
    candidate_id: helpCandidate.id,
    asset: helpCandidate.asset,
    content_hash: helpCandidate.content_hash,
    cv_run_id: "run_help",
    status: "APPROVED_FOR_INTERNAL_PRINTABLE",
    internal_printable_eligible: true,
    publication_status: "DRAFT"
  };
  const workflow = {
    sign_id: "help",
    cv_run_id: "run_help",
    selected_candidate_id: helpCandidate.id,
    visual_review_status: "APPROVED_FOR_INTERNAL_PRINTABLE",
    internal_printable_eligible: true,
    publication_status: "DRAFT"
  };
  const storage = new Map([
    ["kinderflowPrintableApproval", JSON.stringify(approval)],
    ["kinderflowApprovedVisual", JSON.stringify(approvedVisual)],
    ["kinderflowVisualWorkflow", JSON.stringify(workflow)]
  ]);
  const scenario = process.argv[5] || "valid";
  if (scenario === "missing-workflow") storage.delete("kinderflowVisualWorkflow");
  if (scenario === "workflow-candidate-mismatch") {
    storage.set("kinderflowVisualWorkflow", JSON.stringify({ ...workflow, selected_candidate_id: "help-b" }));
  }
  if (scenario === "visual-hash-mismatch") {
    storage.set("kinderflowApprovedVisual", JSON.stringify({ ...approvedVisual, content_hash: "tampered-hash" }));
  }
  if (scenario === "printable-type-mismatch") {
    storage.set("kinderflowPrintableApproval", JSON.stringify({ ...approval, card_type: "routine" }));
  }
  if (scenario === "missing-guidance") {
    const { family_guidance: _omitted, ...withoutGuidance } = approval;
    storage.set("kinderflowPrintableApproval", JSON.stringify(withoutGuidance));
  }

  class FakeSvgDocument {
    constructor(svgSource) {
      this.source = svgSource;
      this.textNodes = [...svgSource.matchAll(/<text\b[^>]*>([^<]*)<\/text>/g)].map((match) => ({
        textContent: match[1]
      }));
      this.documentElement = this;
    }
    querySelector(selector) { return selector === "parsererror" ? null : null; }
    querySelectorAll(selector) { return selector === "text" ? this.textNodes : []; }
  }
  class FakeXmlSerializer {
    serializeToString(svgDocument) {
      let index = 0;
      return svgDocument.source.replace(
        /(<text\b[^>]*>)([^<]*)(<\/text>)/g,
        (_match, open, _text, close) => `${open}${svgDocument.textNodes[index++].textContent}${close}`
      );
    }
  }
  const fetch = async (url) => {
    const value = String(url);
    if (value.endsWith("data/signs.json")) return { ok: true, json: async () => signsPayload };
    if (value.endsWith("data/visual_sign_packages.json")) return { ok: true, json: async () => packagesPayload };
    const assetPath = require("path").join(process.argv[4], value);
    return { ok: true, text: async () => fs.readFileSync(assetPath, "utf8") };
  };
  const context = {
    document,
    window: {
      location: {
        search: `?sign=help&type=flashcard&lang=en&asset=${encodeURIComponent(helpCandidate.id)}&routine=Garden%20tidy-up`
      },
      print() {}
    },
    sessionStorage: {
      getItem(key) { return storage.get(key) || null; },
      setItem(key, value) { storage.set(key, String(value)); }
    },
    fetch,
    URLSearchParams,
    DOMParser: class { parseFromString(value) { return new FakeSvgDocument(value); } },
    XMLSerializer: FakeXmlSerializer,
    encodeURIComponent,
    requestAnimationFrame(callback) { callback(); },
    console
  };
  vm.createContext(context);
  const script = fs.readFileSync(process.argv[1], "utf8");
  vm.runInContext(script + `
;globalThis.__contract = { localizedSvgAsset };
`, context);
  await new Promise((resolve) => setTimeout(resolve, 10));

  const inner = (selector) => element(`#a5-print-card ${selector}`);
  const placeholder = inner("[data-print-context-placeholder]");
  const contextImage = inner("[data-print-context]");
  const signImage = inner("[data-print-sign]");
  const missingContext = {
    cardVisible: !card.hidden,
    errorHidden: element("#print-card-error").hidden,
    printEnabled: !element("#open-print-dialog").disabled,
    word: inner("[data-print-word]").textContent,
    placeholderHidden: placeholder.hidden,
    placeholderText: placeholder.textContent,
    contextImageHidden: contextImage.hidden,
    contextImageSrc: contextImage.src,
    signImageSrc: signImage.src,
    guidance: inner("[data-print-guidance]").textContent,
    returnHref: element("#return-to-builder").href,
    errorMessage: element("#print-card-error-message").textContent
  };

  const localizedUrl = await context.__contract.localizedSvgAsset(moreCandidate.asset, "es");
  const localizedSvg = decodeURIComponent(localizedUrl.split(",", 2)[1]);
  process.stdout.write(JSON.stringify({ missingContext, localizedSvg }));
})().catch((error) => {
  process.stderr.write(error.stack || String(error));
  process.exitCode = 1;
});
'''


class Prompt2CReviewUxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = source("create-sign.html")
        cls.script = source("create-sign.js")
        cls.tree = parse_html("create-sign.html")
        cls.runtime = node_json(
            CREATE_SIGN_HARNESS,
            PROTOTYPE_ROOT / "create-sign.js",
        )

    def test_reference_review_tells_one_concise_review_story(self) -> None:
        review = self.runtime["review"]
        self.assertEqual(review["resultTitle"], "Reference review complete")
        self.assertEqual(
            review["explanation"],
            "We found a few moments worth checking before creating the family materials.",
        )
        self.assertEqual(review["badge"], "Review recommended")
        self.assertEqual(review["warningCount"], 1)
        self.assertNotIn("No child video is required.", self.html)

    def test_tracked_pose_availability_is_enabled_or_explained(self) -> None:
        review = self.runtime["review"]
        self.assertTrue(review["trackedDisabled"])
        self.assertFalse(review["trackedHelpHidden"])
        self.assertEqual(
            self.tree.by_id("tracked-pose-availability").all_text(),
            "Tracked poses aren’t clear enough for this reference. Choose one or two reference frames instead.",
        )
        self.assertFalse(self.runtime["pass"]["trackedDisabled"])
        self.assertTrue(self.runtime["pass"]["trackedHelpHidden"])
        self.assertFalse(self.runtime["threshold"]["missing"])
        self.assertFalse(self.runtime["threshold"]["below"])
        self.assertTrue(self.runtime["threshold"]["exact"])
        self.assertTrue(self.runtime["threshold"]["above"])

        for invalid in (self.runtime["unknownStatus"], self.runtime["missingStatus"]):
            self.assertTrue(invalid["actionHidden"])
            self.assertEqual(invalid["candidates"], 0)

        availability = self.tree.by_id("tracked-pose-availability")
        self.assertNotRegex(availability.all_text(), re.compile(r"threshold|percent", re.I))

    def test_pose_selection_blocks_zero_and_caps_at_two(self) -> None:
        picker = self.tree.by_id("reference-frame-picker")
        self.assertIn("Choose one or two reference poses", picker.all_text())
        self.assertIn("Select the clearest moments to guide the visual.", picker.all_text())
        self.assertEqual(
            self.tree.by_id("frame-picker-help").attrs.get("aria-live"), "polite"
        )

        self.assertTrue(self.runtime["review"]["actionDisabled"])
        self.assertEqual(
            self.runtime["review"]["help"], "Select at least one pose to continue."
        )
        self.assertEqual(self.runtime["one"]["help"], "1 pose selected")
        self.assertFalse(self.runtime["one"]["disabled"])
        self.assertEqual(len(self.runtime["one"]["selected"]), 1)
        self.assertEqual(self.runtime["two"]["help"], "2 poses selected")
        self.assertFalse(self.runtime["two"]["disabled"])
        self.assertEqual(len(self.runtime["two"]["selected"]), 2)
        self.assertFalse(self.runtime["max"]["thirdChecked"])
        self.assertEqual(len(self.runtime["max"]["selected"]), 2)

        css = source("styles.css")
        self.assertIn(".suggested-reference-frames label:has(input:checked)", css)
        self.assertIn(":focus-visible", css)

    def test_value_ctas_and_family_material_preparation_are_concise(self) -> None:
        review = self.runtime["review"]
        self.assertEqual(review["action"], "Create family materials")
        self.assertEqual(review["secondary"], "Use another reference")

        preparation = self.tree.by_id("visual-preparation-section")
        self.assertRegex(
            compact(self.html),
            re.compile(r"Prepare\s*<span[^>]*>MORE</span>\s*family materials"),
        )
        self.assertIn(
            "KinderFlow combines the reviewed sign guidance and selected poses to prepare reusable family materials.",
            preparation.all_text(),
        )
        cards = [
            node
            for node in preparation.descendants()
            if node.tag == "article" and node.parent and node.parent.has_class("grounding-summary")
        ]
        self.assertEqual(len(cards), 3)
        for phrase in (
            "Reviewed sign guidance",
            "Reference poses",
            "KinderFlow illustration",
            "Create visual options",
        ):
            self.assertIn(phrase, self.html + self.script)

        runtime = self.runtime["preparation"]
        self.assertEqual(runtime["reviewed"], "Reviewed sign guidance")
        self.assertEqual(runtime["reviewedStatus"], "Ready")
        self.assertEqual(runtime["poses"], "Reference poses")
        self.assertEqual(runtime["posesStatus"], "2 selected")
        self.assertEqual(runtime["illustration"], "KinderFlow illustration")
        self.assertEqual(runtime["illustrationStatus"], "Ready")

    def test_routine_context_reaches_workflow_approval_and_printable_handoff(self) -> None:
        self.assertEqual(self.runtime["workflow"]["routine_context"], "Playtime")
        self.assertEqual(self.runtime["approvedVisual"]["routine_context"], "Playtime")
        self.assertEqual(self.runtime["preparation"]["routine"], "Playtime")
        query = parse_qs(urlsplit(self.runtime["preparation"]["printableHref"]).query)
        self.assertEqual(query.get("routine"), ["Playtime"])

    def test_choose_different_pose_preserves_the_completed_reference_review(self) -> None:
        locks = self.runtime["decisionLocks"]
        self.assertTrue(all(locks["routes"]))
        self.assertTrue(all(locks["frames"]))
        self.assertTrue(locks["rationale"])
        mutation = self.runtime["lockedMutation"]
        self.assertEqual(mutation["route"], "HUMAN_SELECTED_FRAME")
        self.assertEqual(len(mutation["selected"]), 2)
        self.assertTrue(mutation["workflowUnchanged"])
        self.assertTrue(mutation["approvalUnchanged"])

        reset = self.runtime["poseReset"]
        self.assertEqual(reset["runId"], self.runtime["completedRunId"])
        self.assertEqual(reset["reviewTitle"], "Choose one or two reference poses")
        self.assertIn("reference review is still complete", reset["reviewMessage"])
        self.assertTrue(reset["visualHidden"])
        self.assertTrue(reset["familyHidden"])
        self.assertIsNone(reset["approvedVisual"])
        self.assertIsNone(reset["workflow"]["technical_review_action"])
        self.assertEqual(reset["workflow"]["selected_reference_frames"], [])
        self.assertTrue(reset["routesUnlocked"])
        self.assertTrue(reset["framesUnlocked"])
        self.assertTrue(reset["rationaleUnlocked"])
        before = self.runtime["evidenceBeforePoseReset"]
        self.assertEqual(reset["fetchCount"], before["fetchCount"])
        self.assertTrue(reset["resultVisible"])
        self.assertTrue(reset["reviewVisible"])
        for field in ("referenceVideo", "movementVideo", "timeline", "wrist", "frames", "hand", "storedRun"):
            self.assertEqual(reset[field], before[field], field)
        self.assertTrue(before["illustrativeAvailable"])
        self.assertEqual(before["illustrativeSrc"], "/api/illustrative-videos/more")
        self.assertTrue(reset["illustrativeHidden"])
        self.assertEqual(reset["illustrativeSrc"], "")

    def test_restore_requires_the_exact_approved_visual_state(self) -> None:
        missing_package = self.runtime["missingPackageRestore"]
        self.assertTrue(missing_package["downstreamHidden"])
        self.assertIsNone(missing_package["activePackage"])

        wrong_action = self.runtime["wrongActionRestore"]
        self.assertTrue(wrong_action["downstreamHidden"])
        self.assertIsNone(wrong_action["selectedCandidate"])
        self.assertIsNone(wrong_action["action"])
        self.assertIsNone(wrong_action["approval"])

        for invalid_frames in (
            self.runtime["zeroFrameRestore"],
            self.runtime["threeFrameRestore"],
        ):
            self.assertIsNone(invalid_frames["action"])
            self.assertEqual(invalid_frames["selected"], [])
            self.assertIsNone(invalid_frames["approval"])
            self.assertTrue(invalid_frames["approveDisabled"])

        rejected = self.runtime["rejectedRestore"]
        self.assertTrue(rejected["downstreamHidden"])
        self.assertIsNone(rejected["selectedCandidate"])

        approved = self.runtime["approvedRestore"]
        self.assertFalse(approved["downstreamHidden"])
        self.assertEqual(approved["selectedCandidate"], "more-b")
        self.assertEqual(approved["runId"], self.runtime["completedRunId"])

        full_reset = self.runtime["fullReset"]
        self.assertFalse(full_reset["rationaleDisabled"])
        self.assertIsNone(full_reset["referenceReview"])
        self.assertIsNone(full_reset["workflow"])
        self.assertIsNone(full_reset["approval"])


class Prompt2CPrintableStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.flashcard_html = source("flashcards.html")
        cls.flashcard_script = source("flashcards.js")
        cls.print_html = source("print-card.html")
        cls.print_script = source("print-card.js")
        cls.css = source("styles.css")
        cls.flashcard_tree = parse_html("flashcards.html")
        cls.print_tree = parse_html("print-card.html")
        cls.runtime = node_json(
            FLASHCARD_HARNESS,
            PROTOTYPE_ROOT / "flashcards.js",
        )
        cls.print_runtime = node_json(
            PRINT_CARD_HARNESS,
            PROTOTYPE_ROOT / "print-card.js",
            PROTOTYPE_ROOT / "data/signs.json",
            PROTOTYPE_ROOT / "data/visual_sign_packages.json",
            PROTOTYPE_ROOT,
        )

    def test_flashcard_word_and_visual_are_one_integrated_card(self) -> None:
        cards = self.flashcard_tree.by_class("flashcard-output")
        self.assertEqual(len(cards), 1)
        card = cards[0]
        lockups = [node for node in card.descendants() if node.has_class("flashcard-sign-lockup")]
        self.assertEqual(len(lockups), 1)
        self.assertTrue(
            any(node.attrs.get("data-card-sign") is not None for node in lockups[0].descendants())
        )
        self.assertTrue(any(node.has_class("flashcard-visual") for node in card.descendants()))

        final_card_rule = self.css.rsplit(
            ".flashcard-page .print-sheet .flashcard-output", 1
        )[-1]
        self.assertIn("overflow: hidden", final_card_rule)
        self.assertNotRegex(final_card_rule, r"min-height\s*:\s*6[0-9]{2}px")

    def test_word_lockup_uses_shared_two_axis_centering(self) -> None:
        lockup_rules = re.findall(
            r"(?:\.flashcard-page\s+)?\.flashcard-sign-lockup\s*\{([^}]*)\}",
            self.css,
            re.DOTALL,
        )
        self.assertTrue(lockup_rules)
        centered_rules = [
            rule
            for rule in lockup_rules
            if "place-items: center" in rule
            or (
                "align-items: center" in rule
                and "justify-content: center" in rule
            )
        ]
        self.assertTrue(centered_rules, lockup_rules)
        self.assertTrue(
            any("text-align: center" in rule for rule in lockup_rules)
            or bool(
                re.search(
                    r"\.flashcard-page\s+\.flashcard-sign-lockup\s+(?:h3|p)[\s\S]*?text-align:\s*center",
                    self.css,
                )
            )
        )
        self.assertRegex(
            self.css,
            re.compile(r"\.a5-print-card\s*>\s*h2\s*\{[^}]*place-items:\s*center", re.DOTALL),
        )

    def test_routine_card_keeps_its_established_structure(self) -> None:
        card = self.flashcard_tree.by_class("flashcard-output")[0]
        required_classes = {
            "flashcard-output-header",
            "flashcard-visual-unit",
            "flashcard-visual",
            "flashcard-sign-art",
            "flashcard-sign-lockup",
            "flashcard-routine",
            "flashcard-guidance",
            "routine-card-icon",
        }
        actual = {
            class_name
            for node in card.descendants()
            for class_name in node.attrs.get("class", "").split()
        }
        self.assertTrue(required_classes.issubset(actual), required_classes - actual)

    def test_spanish_card_copy_has_no_known_english_leaks(self) -> None:
        combined = self.flashcard_script + self.print_script
        for translation in (
            "TARJETA DE RUTINA",
            "INICIO",
            "FINAL",
            "JUNTAR · SEPARAR · REPETIR",
        ):
            self.assertIn(translation, combined)
        self.assertIn("MÁS", combined + self.flashcard_html + self.print_html)

        card = self.runtime["spanish"]
        self.assertEqual(card["word"], "MÁS")
        self.assertTrue(card["secondaryHidden"])
        self.assertEqual(card["kind"], "TARJETA DE RUTINA")
        self.assertEqual(card["routineLabel"], "Rutina")
        self.assertEqual(card["routine"], "Hora de jugar")
        self.assertEqual(card["guidanceLabel"], "Cómo usarlo")
        self.assertEqual(card["guidance"], "Guía aprobada.")
        self.assertEqual(card["movement"], "↔ JUNTAR · SEPARAR · REPETIR")
        visible = " ".join(
            str(card[field])
            for field in (
                "word",
                "kind",
                "routineLabel",
                "routine",
                "guidanceLabel",
                "guidance",
                "movement",
                "iconLabel",
            )
        )
        for leak in (r"\bSTART\b", r"\bEND\b", r"\bROUTINE CARD\b", r"\bMEET\b", r"\bSEPARATE\b", r"\bREPEAT\b"):
            self.assertNotRegex(visible, re.compile(leak, re.IGNORECASE))

        accessibility = self.runtime["spanishAccessibility"]
        self.assertEqual(accessibility["signAlt"], "Ilustración revisada del signo MÁS")
        self.assertEqual(accessibility["contextAlt"], "Contexto cotidiano")
        self.assertIn('language === "es" ? copy.context', self.print_script)

        localized_svg = self.print_runtime["localizedSvg"]
        for translation in (
            "INICIO",
            "FINAL",
            "JUNTAR · SEPARAR · REPETIR",
        ):
            self.assertRegex(
                localized_svg,
                re.compile(rf">\s*{re.escape(translation)}\s*<"),
            )
        for leak in (
            "START",
            "END",
            "MEET · SEPARATE · REPEAT",
        ):
            self.assertNotRegex(
                localized_svg,
                re.compile(rf">\s*{re.escape(leak)}\s*<", re.IGNORECASE),
            )

    def test_missing_context_has_neutral_non_image_fallback(self) -> None:
        preview_placeholders = [
            node
            for node in self.flashcard_tree.root.descendants()
            if "data-context-placeholder" in node.attrs
        ]
        print_placeholders = [
            node
            for node in self.print_tree.root.descendants()
            if "data-print-context-placeholder" in node.attrs
        ]
        self.assertEqual(len(preview_placeholders), 1)
        self.assertEqual(len(print_placeholders), 1)
        preview_placeholder = preview_placeholders[0]
        print_placeholder = print_placeholders[0]
        self.assertIn("Context image not prepared yet", preview_placeholder.all_text())
        self.assertIn("Context image not prepared yet", print_placeholder.all_text())
        for implementation in (self.flashcard_script, self.print_script):
            self.assertRegex(
                implementation,
                re.compile(
                    r"\.hidden\s*=\s*true;[\s\S]{0,160}?\.removeAttribute\([\"']src[\"']\)",
                ),
            )
        self.assertNotIn('contextImage.src = visualPackage.contextual_image?.asset || ""', self.flashcard_script)

        missing = self.runtime["custom"]
        self.assertTrue(missing["cardVisible"])
        self.assertTrue(missing["contextImageHidden"])
        self.assertEqual(missing["contextImageSrc"], "")
        self.assertFalse(missing["placeholderHidden"])
        self.assertEqual(missing["placeholderText"], "Context image not prepared yet")
        self.assertTrue(missing["signImageSourceAsset"].endswith("more-b.svg"))

        print_missing = self.print_runtime["missingContext"]
        self.assertTrue(print_missing["cardVisible"])
        self.assertTrue(print_missing["errorHidden"])
        self.assertTrue(print_missing["printEnabled"])
        self.assertEqual(print_missing["word"], "HELP")
        self.assertTrue(print_missing["contextImageHidden"])
        self.assertEqual(print_missing["contextImageSrc"], "")
        self.assertFalse(print_missing["placeholderHidden"])
        self.assertEqual(
            print_missing["placeholderText"],
            "Context image not prepared yet",
        )
        self.assertTrue(print_missing["signImageSrc"].startswith("data:image/svg+xml"))
        self.assertEqual(print_missing["guidance"], "Approved guidance snapshot.")

    def test_print_return_restores_the_exact_approved_printable(self) -> None:
        combined = self.flashcard_script + self.print_script
        for field in (
            "sign_id",
            "candidate_id",
            "asset",
            "content_hash",
            "language",
            "card_type",
            "routine_context",
            "family_guidance",
        ):
            self.assertIn(field, combined)
        self.assertIn('status: "PRINTABLE_READY"', self.flashcard_script)
        self.assertEqual(
            self.runtime["savedPrintable"]["family_guidance"],
            {
                "en": "Use the sign naturally during the routine.",
                "es": "Usa el signo de forma natural durante la rutina.",
            },
        )
        self.assertRegex(self.print_script, r'approved:\s*["\']1["\']')
        self.assertRegex(self.print_script, r'restore:\s*["\']1["\']')
        for copy in ("Printable ready", "Print / Save as PDF", "Create another format", "Back to family materials"):
            self.assertIn(copy, self.flashcard_html + self.flashcard_script)

        restored = self.runtime["spanish"]
        self.assertTrue(restored["ready"])
        self.assertEqual(restored["readyText"], "Printable ready")
        self.assertEqual(restored["printText"], "Print / Save as PDF")
        self.assertFalse(restored["postActionsHidden"])
        print_query = parse_qs(urlsplit(self.runtime["printHref"]).query)
        self.assertEqual(print_query.get("sign"), ["more"])
        self.assertEqual(print_query.get("type"), ["routine"])
        self.assertEqual(print_query.get("lang"), ["es"])
        self.assertEqual(print_query.get("asset"), ["more-b"])
        self.assertEqual(print_query.get("routine"), ["Playtime"])

        return_query = parse_qs(
            urlsplit(self.print_runtime["missingContext"]["returnHref"]).query
        )
        self.assertEqual(return_query.get("approved"), ["1"])
        self.assertEqual(return_query.get("restore"), ["1"])
        self.assertEqual(return_query.get("sign"), ["help"])
        self.assertEqual(return_query.get("type"), ["flashcard"])
        self.assertEqual(return_query.get("lang"), ["en"])
        self.assertEqual(return_query.get("routine"), ["Garden tidy-up"])
        self.assertEqual(return_query.get("asset"), ["help-a"])
        self.assertEqual(return_query.get("visual"), ["help-a"])

        trust = self.runtime["trust"]
        self.assertFalse(trust["missingWorkflow"])
        self.assertFalse(trust["wrongWorkflowCandidate"]["loaded"])
        self.assertFalse(trust["wrongWorkflowCandidate"]["candidate"])
        self.assertTrue(trust["wrongVisualHash"]["loaded"])
        self.assertFalse(trust["wrongVisualHash"]["candidate"])
        self.assertFalse(trust["wrongWorkflowPublication"]["loaded"])
        self.assertFalse(trust["wrongWorkflowPublication"]["candidate"])
        self.assertFalse(trust["printableTrust"]["wrongCandidate"])
        self.assertFalse(trust["printableTrust"]["wrongType"])
        self.assertFalse(trust["printableTrust"]["wrongLanguage"])
        self.assertEqual(self.runtime["stalePrintableOutput"]["routine"], "Playtime")
        self.assertEqual(
            self.runtime["stalePrintableOutput"]["guidance"],
            "Use the sign naturally during the routine.",
        )
        pending = self.runtime["pendingAsset"]
        self.assertTrue(pending["approveDisabled"])
        self.assertIsNone(pending["printableBeforeClick"])
        self.assertIsNone(pending["printableAfterClick"])

    def test_print_proof_fails_closed_for_mismatched_saved_state(self) -> None:
        for scenario in (
            "missing-workflow",
            "workflow-candidate-mismatch",
            "visual-hash-mismatch",
            "printable-type-mismatch",
            "missing-guidance",
        ):
            with self.subTest(scenario=scenario):
                runtime = node_json(
                    PRINT_CARD_HARNESS,
                    PROTOTYPE_ROOT / "print-card.js",
                    PROTOTYPE_ROOT / "data/signs.json",
                    PROTOTYPE_ROOT / "data/visual_sign_packages.json",
                    PROTOTYPE_ROOT,
                    Path(scenario),
                )["missingContext"]
                self.assertFalse(runtime["cardVisible"])
                self.assertFalse(runtime["errorHidden"])
                self.assertFalse(runtime["printEnabled"])
                self.assertIn("Approve this exact card", runtime["errorMessage"])

    def test_create_another_format_preserves_the_approved_visual(self) -> None:
        match = re.search(
            r'querySelector\(["\']#create-another["\']\)\.addEventListener\([\s\S]+?\n\}\);',
            self.flashcard_script,
        )
        self.assertIsNotNone(match)
        handler = match.group(0) if match else ""
        for forbidden_reset in (
            "builder.selectedId = null",
            "builder.approvedVisual = null",
            "sessionStorage.removeItem(\"kinderflowApprovedVisual\")",
        ):
            self.assertNotIn(forbidden_reset, handler)
        self.assertEqual(
            self.runtime["beforeAnother"]["selectedId"],
            self.runtime["afterAnother"]["selectedId"],
        )
        self.assertEqual(
            self.runtime["beforeAnother"]["candidateId"],
            self.runtime["afterAnother"]["candidateId"],
        )
        self.assertEqual(
            self.runtime["beforeAnother"]["asset"],
            self.runtime["afterAnother"]["asset"],
        )
        self.assertIsNone(self.runtime["afterAnother"]["printableApproval"])

    def test_known_routines_translate_and_unknown_spanish_text_uses_reviewed_fallback(self) -> None:
        combined = self.flashcard_script + self.print_script
        for english, spanish in (
            ("Snack time", "Hora de la merienda"),
            ("Playtime", "Hora de jugar"),
            ("Mealtime", "Hora de comer"),
        ):
            self.assertIn(english.lower(), combined.lower())
            self.assertIn(spanish, combined)
        self.assertNotIn("MORE_ROUTINE_COPY", self.flashcard_script)
        self.assertRegex(
            combined,
            re.compile(r"routine_context", re.IGNORECASE),
        )
        self.assertEqual(self.runtime["translations"]["snack"], "Hora de la merienda")
        self.assertEqual(self.runtime["translations"]["play"], "Hora de jugar")
        self.assertEqual(self.runtime["translations"]["meal"], "Hora de comer")
        self.assertEqual(self.runtime["translations"]["custom"], "")
        self.assertEqual(self.runtime["translations"]["mixed"], "")
        self.assertEqual(self.runtime["custom"]["routine"], "Garden tidy-up")
        self.assertEqual(
            self.runtime["savedPrintable"]["routine_context"],
            {"en": "Garden tidy-up", "es": "Hora de la merienda"},
        )
        self.assertEqual(self.runtime["savedPrintable"]["candidate_id"], "more-b")


class Prompt2CPreservedBehaviorTests(unittest.TestCase):
    def test_water_routing_and_unknown_sign_fail_closed(self) -> None:
        packages = json.loads(source("data/visual_sign_packages.json"))["signs"]
        water = next(item for item in packages if item["sign_id"] == "water")
        candidates = water.get("candidates", []) + water.get(
            "regeneration_candidates", []
        )
        self.assertTrue(candidates)
        for candidate in candidates:
            self.assertTrue(candidate["id"].startswith("water"))
            self.assertNotIn("more", candidate["asset"].lower())

        create_sign = source("create-sign.js")
        self.assertNotRegex(create_sign, r"(?:activePackage|signPackage)\s*\|\|\s*[^;\n]*more")
        self.assertIn("This sign is not available in the current demo set.", create_sign)

    def test_story_language_contract_is_unchanged(self) -> None:
        html = source("create-story.html")
        script = source("story.js")
        selector = re.search(
            r'<select\b[^>]*id=["\']story-language["\'][^>]*>(.*?)</select>',
            html,
            re.IGNORECASE | re.DOTALL,
        )
        self.assertIsNotNone(selector)
        choices = selector.group(1) if selector else ""
        self.assertRegex(choices, r'value=["\']en["\']')
        self.assertRegex(choices, r'value=["\']es["\']')
        self.assertIn('requestedSign !== "more"', script)
        self.assertIn("A story has not been prepared for this sign yet.", script)

    @unittest.skipUnless(shutil.which("node"), "Node is unavailable")
    def test_javascript_syntax_html_css_and_diff_contracts(self) -> None:
        for script in sorted(PROTOTYPE_ROOT.glob("*.js")):
            with self.subTest(script=script.name):
                result = subprocess.run(
                    [shutil.which("node") or "node", "--check", str(script)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

        for name in ("create-sign.html", "flashcards.html", "print-card.html"):
            tree = parse_html(name)
            ids = [
                node.attrs["id"]
                for node in tree.root.descendants()
                if node.attrs.get("id")
            ]
            self.assertEqual(len(ids), len(set(ids)), name)

        css = source("styles.css")
        self.assertIn("prefers-reduced-motion: reduce", css)
        self.assertIn(":focus-visible", css)
        self.assertRegex(css, r"min-height\s*:\s*(?:44|48)px")
        self.assertRegex(css, r"@media\s*\(max-width:\s*(?:760|768)px\)")

        result = subprocess.run(
            ["git", "diff", "--check"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
