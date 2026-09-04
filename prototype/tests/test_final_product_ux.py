from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PROTOTYPE_ROOT = REPO_ROOT / "prototype"


def source(name: str) -> str:
    return (PROTOTYPE_ROOT / name).read_text(encoding="utf-8")


def element_body(html: str, tag: str, attribute: str, value: str) -> str:
    match = re.search(
        rf'<{tag}\b[^>]*\b{re.escape(attribute)}=["\']{re.escape(value)}["\'][^>]*>(.*?)</{tag}>',
        html,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        raise AssertionError(f"Missing {tag}[{attribute}={value}]")
    return match.group(1)


def node_json(harness: str, *arguments: str | Path) -> dict:
    node = shutil.which("node")
    if not node:
        raise unittest.SkipTest("Node is unavailable")
    result = subprocess.run(
        [node, "-e", harness, *[str(argument) for argument in arguments]],
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


SCHOOL_ASSIGNMENT_HARNESS = r'''
const fs = require("fs");
const vm = require("vm");

let elementSequence = 0;
class Element {
  constructor(key, tagName = "div") {
    this.key = key;
    this.tagName = tagName.toLowerCase();
    this.children = [];
    this.listeners = {};
    this.attributes = {};
    this.dataset = {};
    this.className = "";
    this.textContent = "";
    this.type = "";
    this.name = "";
    this.value = "";
    this.checked = false;
    this.hidden = false;
    this.disabled = false;
    this.focused = false;
  }
  addEventListener(type, listener) { (this.listeners[type] ||= []).push(listener); }
  dispatch(type, overrides = {}) {
    const event = {
      currentTarget: this,
      target: this,
      preventDefault() {},
      ...overrides
    };
    for (const listener of this.listeners[type] || []) listener(event);
  }
  append(...children) {
    for (const child of children) {
      if (child && typeof child === "object") child.parent = this;
      this.children.push(child);
    }
  }
  prepend(...children) {
    for (const child of children) {
      if (child && typeof child === "object") child.parent = this;
    }
    this.children.unshift(...children);
    if (this.tagName === "select") this.value = children[0]?.value || this.value;
  }
  replaceChildren(...children) {
    this.children = [];
    this.append(...children);
    if (this.tagName === "select") {
      const selected = children.find((child) => child?.selected || child?.defaultSelected) || children[0];
      this.value = selected?.value || "";
    }
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
  querySelectorAll(selector) {
    if (selector === 'input[name="materials"]:checked') {
      return this.walk().filter((item) => item.tagName === "input" && item.name === "materials" && item.checked);
    }
    if (selector === "[data-assignment-id]") {
      return this.walk().filter((item) => Object.hasOwn(item.dataset, "assignmentId"));
    }
    return [];
  }
  querySelector(selector) {
    if (selector === "input") return this.walk().find((item) => item.tagName === "input") || null;
    const assignmentId = selector.match(/^\[data-assignment-id="(.*)"\]$/)?.[1];
    if (assignmentId !== undefined) {
      return this.walk().find((item) => String(item.dataset.assignmentId) === assignmentId) || null;
    }
    return null;
  }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return this.attributes[name] ?? null; }
  matches(selector) {
    if (selector === "[data-edit-assignment]") return Object.hasOwn(this.dataset, "editAssignment");
    if (selector === "[data-remove-assignment]") return Object.hasOwn(this.dataset, "removeAssignment");
    return false;
  }
  closest(selector) {
    let node = this;
    while (node) {
      if (node.matches?.(selector)) return node;
      node = node.parent;
    }
    return null;
  }
  focus() { this.focused = true; }
  scrollIntoView() {}
}

class OptionElement extends Element {
  constructor(text, value, defaultSelected = false, selected = false) {
    super(`option-${++elementSequence}`, "option");
    this.text = text;
    this.textContent = text;
    this.value = value;
    this.defaultSelected = defaultSelected;
    this.selected = selected;
  }
}

const nodes = new Map();
const make = (selector, tagName = "div", values = {}) => {
  const node = Object.assign(new Element(selector, tagName), values);
  nodes.set(selector, node);
  return node;
};

const assignmentForm = make("#school-assignment-form", "form");
const signSelect = make("#assignment-sign", "select", { value: "more" });
const groupSelect = make("#assignment-group", "select", { value: "Group 1–2" });
const materialChoices = make("#assignment-materials");
const childPanel = make("#assignment-child-panel", "div", { hidden: true });
const childSelect = make("#assignment-child", "select", { disabled: true });
make("#school-assignment-status");
make("#assignment-summary");
make("#assignment-material-summary");
make("#assignment-validation");
make("#assignment-submit", "button");
const assignmentResult = make(".assignment-result", "div", { hidden: true });
const duplicatePanel = make("#duplicate-assignment", "div", { hidden: true });
make("#assign-another", "button");
make("#cancel-assignment-edit", "button", { hidden: true });
const activeList = make("#active-sign-list");
make("#view-active-assignment", "button");
make("#change-assignment-materials", "button");
make("#view-family-experience", "a", { href: "family.html" });

const groupAudience = Object.assign(new Element("audience-group", "input"), {
  name: "audience", value: "group", checked: true
});
const childAudience = Object.assign(new Element("audience-child", "input"), {
  name: "audience", value: "child", checked: false
});
const audiences = [groupAudience, childAudience];

const document = {
  querySelector(selector) {
    if (selector === 'input[name="audience"]:checked') {
      return audiences.find((input) => input.checked) || null;
    }
    const audienceValue = selector.match(/^input\[name="audience"\]\[value="([^\"]+)"\]$/)?.[1];
    if (audienceValue) return audiences.find((input) => input.value === audienceValue) || null;
    return nodes.get(selector) || null;
  },
  querySelectorAll(selector) {
    if (selector === 'input[name="audience"]') return audiences;
    if (selector === "[data-select-library-sign]") return [];
    return [];
  },
  createElement(tagName) { return new Element(`created-${tagName}-${++elementSequence}`, tagName); }
};

const storage = new Map();
if (process.argv[2]) storage.set("kinderflowPrintableApproval", process.argv[2]);
const context = {
  document,
  window: { location: { search: process.argv[3] || "" }, matchMedia: () => ({ matches: false }) },
  sessionStorage: {
    getItem(key) { return storage.has(key) ? storage.get(key) : null; },
    setItem(key, value) { storage.set(key, String(value)); }
  },
  URLSearchParams,
  Option: OptionElement,
  console
};
vm.createContext(context);
const code = fs.readFileSync(process.argv[1], "utf8");
vm.runInContext(code + `
;globalThis.__contract = {
  snapshot() { return JSON.parse(JSON.stringify(assignments)); },
  startEditingAssignment
};`, context);

const contract = context.__contract;
const snapshot = () => contract.snapshot();
const storedAssignments = () => JSON.parse(storage.get("kinderflowSchoolAssignments") || "[]");
const findCard = (id) => activeList.children.find((card) => card.dataset.assignmentId === id);
const findAction = (card, key, id) => card.walk().find((item) => item.dataset[key] === id);

const initialSelection = {
  sign: signSelect.value,
  group: groupSelect.value,
  materials: materialChoices.walk()
    .filter((item) => item.name === "materials" && item.checked)
    .map((item) => item.value),
  focused: signSelect.focused,
  validation: nodes.get("#assignment-validation").textContent
};

const initialCount = snapshot().length;
assignmentForm.dispatch("submit");
const afterFirstShare = snapshot();
const toddlerAssignment = afterFirstShare.find((item) => item.id !== "seed-more-babies");
const firstResultVisible = !assignmentResult.hidden;
const firstStoredCount = storedAssignments().length;
const firstFamilyContext = JSON.parse(storage.get("kinderflowFamilyPreviewAssignmentId") || "null");
const firstFamilyHref = nodes.get("#view-family-experience")?.href || "";

assignmentForm.dispatch("submit");
const duplicateCount = snapshot().length;
const duplicateShown = !duplicatePanel.hidden;

groupSelect.value = "Group 2–3";
groupSelect.dispatch("change");
assignmentForm.dispatch("submit");
const afterDifferentGroup = snapshot();
const preschoolAssignment = afterDifferentGroup.find((item) => item.groupId === "Group 2–3");
const differentGroupAllowed = afterDifferentGroup.length === afterFirstShare.length + 1;
const resultVisibleBeforeDraftChange = !assignmentResult.hidden;

groupAudience.checked = false;
childAudience.checked = true;
childAudience.dispatch("change");
const resultHiddenAfterDraftChange = assignmentResult.hidden;
const childShown = !childPanel.hidden && !childSelect.disabled;
childSelect.value = "Child E";
childSelect.dispatch("change");
groupAudience.checked = true;
childAudience.checked = false;
groupAudience.dispatch("change");
const childReset = childPanel.hidden && childSelect.disabled && childSelect.value === "";

const editCard = findCard(preschoolAssignment.id);
const editButton = findAction(editCard, "editAssignment", preschoolAssignment.id);
activeList.dispatch("click", { target: editButton });
const routineChoice = materialChoices.walk().find((item) => item.name === "materials" && item.value === "routine-card");
routineChoice.checked = false;
materialChoices.dispatch("change");
const countBeforeEdit = snapshot().length;
assignmentForm.dispatch("submit");
const afterEdit = snapshot();
const edited = afterEdit.find((item) => item.id === preschoolAssignment.id);
const editInPlace = afterEdit.length === countBeforeEdit
  && edited?.id === preschoolAssignment.id
  && JSON.stringify(edited.materials) === JSON.stringify(["video", "flashcard"]);

const updatedCard = findCard(preschoolAssignment.id);
const updatedEdit = findAction(updatedCard, "editAssignment", preschoolAssignment.id);
const updatedRemove = findAction(updatedCard, "removeAssignment", preschoolAssignment.id);
const editLabel = updatedEdit?.getAttribute("aria-label") || updatedEdit?.ariaLabel || "";
const removeLabel = updatedRemove?.getAttribute("aria-label") || updatedRemove?.ariaLabel || "";
activeList.dispatch("click", { target: updatedRemove });
const afterRemove = snapshot();
const storedAfterRemove = storedAssignments();

process.stdout.write(JSON.stringify({
  initialSelection,
  initialCount,
  firstShareCount: afterFirstShare.length,
  firstStoredCount,
  firstResultVisible,
  firstFamilyContext,
  firstFamilyHref,
  toddlerAssignment,
  duplicateCount,
  duplicateShown,
  differentGroupAllowed,
  resultVisibleBeforeDraftChange,
  resultHiddenAfterDraftChange,
  childShown,
  childReset,
  editInPlace,
  editLabel,
  removeLabel,
  removed: !afterRemove.some((item) => item.id === preschoolAssignment.id),
  removeCount: afterRemove.length,
  storedRemoveCount: storedAfterRemove.length,
  storedRemoved: !storedAfterRemove.some((item) => item.id === preschoolAssignment.id)
}));
'''


SCHOOL_RESTORE_HARNESS = r'''
const fs = require("fs");
const vm = require("vm");
const saved = process.argv[2];
const context = {
  document: { querySelector: () => null, querySelectorAll: () => [] },
  window: { location: { search: "" }, matchMedia: () => ({ matches: false }) },
  sessionStorage: {
    getItem(key) { return key === "kinderflowSchoolAssignments" ? saved : null; },
    setItem() {}
  },
  URLSearchParams,
  Option: class {},
  console
};
vm.createContext(context);
const code = fs.readFileSync(process.argv[1], "utf8");
vm.runInContext(code + `
;globalThis.__restored = {
  ids: assignments.map((assignment) => assignment.id),
  assignmentSequence,
  nextId: nextAssignmentId(),
  sequenceAfterNext: assignmentSequence
};`, context);
process.stdout.write(JSON.stringify(context.__restored));
'''


class FinalProductUxStaticTests(unittest.TestCase):
    def test_studio_navigation_keeps_family_formats_as_outputs(self) -> None:
        for page in (
            "admin.html",
            "content-studio.html",
            "create-sign.html",
            "flashcards.html",
            "create-story.html",
            "create-song.html",
            "library.html",
        ):
            html = source(page)
            nav = re.search(r"<nav\b[^>]*>(.*?)</nav>", html, re.IGNORECASE | re.DOTALL)
            self.assertIsNotNone(nav, page)
            navigation = nav.group(1) if nav else ""
            for label in ("Overview", "Kinder Signs", "Content Library", "Schools"):
                self.assertIn(label, navigation, page)
            self.assertIn('href="admin.html"', navigation, page)
            self.assertIn('href="content-studio.html"', navigation, page)
            self.assertIn('href="library.html"', navigation, page)
            self.assertIn('href="school.html"', navigation, page)
            for removed in ("Create Flashcard", "Create Story", "Create Song"):
                self.assertNotIn(removed, navigation, page)

        family = element_body(source("create-sign.html"), "section", "id", "downstream-section")
        for heading in ("Flashcard", "Routine Card", "Story", "Song"):
            self.assertRegex(family, rf"<h3>{re.escape(heading)}</h3>")
        self.assertIn("Continue from the same reviewed sign; no reference work is lost.", family)
        self.assertNotIn("library.html", family.lower())
        song = re.search(
            r'<article\b[^>]*is-coming-soon[^>]*>(.*?)</article>',
            family,
            re.IGNORECASE | re.DOTALL,
        )
        self.assertIsNotNone(song)
        song_body = song.group(1) if song else ""
        self.assertIn("Coming soon", song_body)
        self.assertNotRegex(song_body, r"<(?:a|button)\b")

    def test_platform_and_product_bridge_present_one_clear_story(self) -> None:
        platform = source("index.html")
        product = source("kinder-signs.html")
        studio = source("content-studio.html")

        for label in ("KinderFlow", "Products", "How it works", "For nurseries"):
            self.assertIn(label, element_body(platform, "nav", "aria-label", "Platform navigation"))
            self.assertIn(label, element_body(product, "nav", "aria-label", "Platform navigation"))
        self.assertRegex(platform, r'href="kinder-signs\.html"[^>]*>Explore Kinder Signs</a>')
        for copy in (
            "Bring nursery learning home.",
            "Nursery centres",
            "Children reached",
            "Signs available",
            "Video tutorials",
            "KinderFlow prepares",
            "The nursery chooses",
            "Families use it at home",
        ):
            self.assertIn(copy, platform)
        for copy in (
            "Save production time",
            "Reuse your expertise",
            "Create new revenue opportunities",
            "MediaPipe landmarks",
            "Human review",
            "Create a sign",
            "Open sign library",
        ):
            self.assertIn(copy, product)
        self.assertEqual(product.count('data-sign-id="'), 6)
        self.assertIn("Choose the product your team wants to create or manage.", studio)
        self.assertIn("Kinder Signs", studio)
        self.assertEqual(studio.count('class="studio-product-card '), 3)
        self.assertEqual(studio.count("Coming soon"), 2)
        studio_headings = re.findall(r"<h3>(.*?)</h3>", studio, re.IGNORECASE | re.DOTALL)
        self.assertFalse(any(re.search(r"Flashcard|Story|Song", heading) for heading in studio_headings))

    def test_three_profiles_have_distinct_navigation(self) -> None:
        platform = element_body(source("index.html"), "nav", "aria-label", "Platform navigation")
        team = element_body(source("content-studio.html"), "nav", "aria-label", "KinderFlow Team navigation")
        nursery = element_body(source("school.html"), "nav", "aria-label", "Nursery navigation")
        family = element_body(source("family.html"), "nav", "aria-label", "Family navigation")
        for nav, expected in (
            (platform, ("KinderFlow", "Products", "How it works", "For nurseries")),
            (team, ("Overview", "Kinder Signs", "Content Library", "Schools")),
            (nursery, ("Home", "Available content", "Share", "Active", "Families")),
            (family, ("Your signs", "Your materials")),
        ):
            labels = tuple(re.sub(r"<[^>]+>", "", value).strip() for value in re.findall(r"<a\b[^>]*>(.*?)</a>", nav, re.DOTALL))
            self.assertEqual(labels, expected)
        self.assertEqual(len({platform, team, nursery, family}), 4)

    def test_create_sign_has_five_visible_stages_and_preserves_evidence(self) -> None:
        html = source("create-sign.html")
        script = source("create-sign.js")
        self.assertEqual(html.count("data-product-step="), 5)
        for copy in (
            "Sign &amp; reference",
            "Review reference",
            "Choose poses",
            "Approve visual",
            "Family materials",
            "Step 1 of 5",
            "View processing details",
        ):
            self.assertIn(copy, html)
        processing = element_body(html, "details", "class", "processing-details")
        self.assertIn('id="processing-stages"', processing)
        for protected_id in (
            "reference-video-preview",
            "movement-video-preview",
            "metric-frames",
            "metric-pose",
            "metric-hand",
            "metric-missing",
            "metric-unresolved",
            "detection-timeline",
            "wrist-trajectory",
            "suggested-reference-frames",
            "technical-review-rationale",
            "illustrative-video",
        ):
            self.assertIn(f'id="{protected_id}"', html)
        self.assertIn("TRACKED_POSE_MINIMUM_PERCENT = 90", script)
        self.assertEqual(script.count('textContent = "Pose choice saved"'), 2)
        self.assertNotIn('textContent = "Family materials ready"', script)
        self.assertLess(html.index('id="visual-review-section"'), html.index('id="illustrative-motion-section"'))
        self.assertLess(html.index('id="illustrative-motion-section"'), html.index('id="downstream-section"'))
        self.assertIn("This illustrative video was prepared separately with Google Labs / Gemini.", html)
        stages = element_body(html, "ol", "aria-label", "Create a Sign production stages")
        self.assertNotIn("Library", stages)
        family_video = html.index('id="illustrative-motion-section"')
        flashcard = html.index('id="create-printable-link"')
        self.assertLess(family_video, flashcard)
        self.assertRegex(
            script,
            r'view === "family-materials" && !illustrativeMotionSection\.hidden[\s\S]*?\? illustrativeMotionSection',
        )

    def test_reference_review_copy_status_and_details_contract(self) -> None:
        html = source("create-sign.html")
        script = source("create-sign.js")
        self.assertNotIn('id="reference-status"', html)
        self.assertIn("Reference source", html)
        self.assertIn("Reviewed reference", html)
        self.assertIn("Reference review complete", html + script)
        self.assertIn(
            "We found a few moments worth checking before creating the family materials.",
            html + script,
        )
        self.assertEqual(html.count(">Review recommended<"), 1)
        self.assertIn("What the reference review helps with", html)
        self.assertIn("Find the clearest moments in the sign", html)
        self.assertIn("Final sign approval remains a human decision.", html)
        self.assertNotRegex(html, re.compile(r">\s*Movement check\s*<", re.IGNORECASE))

        details_tag = re.search(r'<details\b[^>]*id="technical-details"[^>]*>', html)
        self.assertIsNotNone(details_tag)
        self.assertNotRegex(details_tag.group(0) if details_tag else "", r"\bopen\b")
        self.assertIn("Advanced run details", html)
        self.assertRegex(
            html,
            re.compile(r"Advanced run details[\s\S]*?<dt>Run ID</dt>", re.IGNORECASE),
        )

    def test_decision_charts_have_purpose_and_why_copy(self) -> None:
        html = source("create-sign.html")
        expected = (
            "Tracking coverage",
            "Shows where the reference pose and main hand were visible across the video.",
            "Gaps help you decide whether to use tracked poses or choose clearer reference frames.",
            "Hand movement path",
            "Shows how the main hand moved relative to the body.",
            "Use it to compare movement direction and identify stable moments for visual preparation.",
        )
        for copy in expected:
            self.assertIn(copy, html)
        self.assertEqual(html.count('class="why-it-matters"'), 2)

    def test_story_song_and_printable_language_contracts(self) -> None:
        story = source("create-story.html")
        for copy in (
            "Turn a reviewed sign into a simple story",
            "Create a short story that helps families practise a sign already introduced at nursery through a familiar everyday routine.",
            "Story guidelines",
            "Original Kinder Signs content",
            "No third-party characters",
            "No medical or developmental claims",
            "Story for shared reading",
        ):
            self.assertIn(copy, story)
        self.assertNotIn("Demo story draft", story)
        self.assertIn("Cuento para leer en familia", source("story.js"))

        song = source("create-song.html")
        self.assertIn("Coming soon", song)
        self.assertIn("Use repetition and rhythm to practise familiar signs through songs.", song)
        self.assertNotRegex(song, re.compile(r">\s*Create song(?: draft)?\s*<", re.IGNORECASE))

        printables = source("flashcards.html") + source("flashcards.js") + source("print-card.html") + source("print-card.js")
        for copy in (
            "Bilingual",
            "Spanish",
            "Finish your printable",
            "Ready for approval",
            "Check the layout and content, then approve the printable before saving it as a PDF.",
            "Approve printable",
            "Back to visual options",
            "Printable ready",
            "Print / Save as PDF",
            "Create another format",
            "Back to family materials",
        ):
            self.assertIn(copy, printables)
        for copy in (
            "Next AI visual milestone",
            "Use generative AI to create and refine KinderFlow-style sign illustrations",
            "Make available to a nursery",
            "Create another sign",
        ):
            self.assertIn(copy, printables)
        for field in (
            "sign_id",
            "sign_label_en",
            "sign_label_es",
            "approved_visual",
            "illustrative_video_available",
            "selected_materials",
            "audience_type",
            "assignment_id",
        ):
            self.assertIn(field, printables)
        self.assertIn('focus: "share"', printables)
        self.assertNotRegex(printables, re.compile(r"\bPNG\b", re.IGNORECASE))

    def test_school_library_and_assignment_structure(self) -> None:
        html = source("school.html")
        css = source("styles.css")
        script = source("school.js")
        self.assertIn("Little Steps Nursery", html)
        self.assertIn("Kinder Signs workspace", html)
        self.assertIn("Share Kinder Signs with your families", html)
        self.assertIn("Choose a sign, select the materials and decide who should receive them.", html)
        self.assertNotRegex(html, re.compile(r"\bSchool A\b|fictional records", re.IGNORECASE))
        self.assertIn("<summary>Demo details</summary>", html)
        for metric_id in (
            "school-metric-groups",
            "school-metric-families",
            "school-metric-materials",
            "school-metric-assignments",
        ):
            self.assertIn(f'id="{metric_id}"', html)

        expected_formats = {
            "more": {"Baby Sign video tutorial", "Flashcard", "Routine Card", "Story"},
            "help": {"Baby Sign video tutorial", "Flashcard", "Routine Card"},
            "eat": {"Flashcard", "Routine Card"},
            "sleep": {"Flashcard", "Routine Card"},
            "milk": {"Baby Sign video tutorial", "Flashcard", "Routine Card"},
            "water": {"Flashcard", "Routine Card"},
        }
        self.assertEqual(html.count('class="school-library-card"'), 6)
        self.assertEqual(html.count('class="status-pill status-neutral">Demo preview</span>'), 6)
        for sign_id, formats in expected_formats.items():
            card = element_body(html, "article", "data-school-sign-card", sign_id)
            rendered = set(re.findall(r"<li>([^<]+)</li>", card))
            self.assertEqual(rendered, formats, sign_id)
            self.assertIn("Demo preview", card)
            self.assertRegex(card, rf'aria-label="{sign_id.upper()} available formats"')
            self.assertNotIn("Song", card)

        for label in ("Sign", "Group", "Materials", "Audience"):
            self.assertIn(label, html)
        child_panel = re.search(
            r'<div\b[^>]*id="assignment-child-panel"[^>]*>(.*?)</div>',
            html,
            re.IGNORECASE | re.DOTALL,
        )
        self.assertIsNotNone(child_panel)
        opening = html[child_panel.start():html.find(">", child_panel.start()) + 1] if child_panel else ""
        self.assertIn("hidden", opening)
        self.assertIn("disabled", child_panel.group(1) if child_panel else "")
        materials = element_body(html, "div", "id", "assignment-materials")
        self.assertNotIn("Song", materials)
        for copy in (
            "This exact sign, audience and material combination is already active.",
            "View active assignment",
            "Change materials",
            "Edit",
            "Remove",
            "View family experience",
            "Share another sign",
            "Who has access to what",
        ):
            self.assertIn(copy, html + script)
        self.assertIn('sessionStorage.setItem("kinderflowFamilyPreviewAssignmentId"', script)
        self.assertIn('sessionStorage.setItem("kinderflowSchoolAssignments"', script)

        self.assertRegex(css, r"\.school-library-grid\s*\{[^}]*repeat\(3,")
        self.assertRegex(
            css,
            re.compile(r"@media \(max-width: 1000px\) and \(min-width: 761px\)[\s\S]*?\.school-library-grid[\s\S]*?repeat\(2,", re.MULTILINE),
        )
        self.assertRegex(
            css,
            re.compile(r"@media \(max-width: 760px\)[\s\S]*?\.school-library-grid[\s\S]*?grid-template-columns: 1fr", re.MULTILINE),
        )

    def test_library_and_family_use_truthful_shared_materials(self) -> None:
        library = source("library.html")
        family = source("family.html")
        family_script = source("app.js")
        self.assertEqual(library.count("data-library-sign-card="), 6)
        for sign in ("MORE", "HELP", "MILK", "EAT", "SLEEP", "WATER"):
            self.assertIn(sign, library)
        for sign in ("more", "help", "milk"):
            card = element_body(library, "article", "data-library-sign-card", sign)
            self.assertIn("Illustrative preview available", card)
        for sign in ("eat", "sleep", "water"):
            card = element_body(library, "article", "data-library-sign-card", sign)
            self.assertIn("Not available yet", card)

        self.assertIn("Your Kinder Signs", family)
        self.assertIn("Shared by Little Steps Nursery", family)
        self.assertIn("No Kinder Signs have been shared with this family yet.", family)
        for forbidden in ("landmarks", "review status", "add-ons", "packs", "internal approval"):
            self.assertNotIn(forbidden, family.lower())
        self.assertNotRegex(family, re.compile(r"\bAI\b|\bplan\b", re.IGNORECASE))
        for copy in (
            "Say the word with the sign",
            "Keep it natural",
            "Follow your child’s interest",
            "Never force repetition",
        ):
            self.assertIn(copy, family)
        self.assertIn('sessionStorage.getItem("kinderflowSchoolAssignments")', family_script)
        self.assertIn("if (raw === null)", family_script)
        self.assertIn("Array.isArray(parsed)", family_script)
        self.assertIn("Video tutorial not available yet. Use the Flashcard or Routine Card instead.", family_script)


@unittest.skipUnless(shutil.which("node"), "Node is unavailable")
class FinalProductAssignmentLogicTests(unittest.TestCase):
    def test_printable_handoff_preselects_sign_formats_group_and_share_focus(self) -> None:
        handoff = {
            "status": "PRINTABLE_READY",
            "publication_status": "DRAFT",
            "sign_id": "more",
            "card_type": "flashcard",
            "language": "en",
            "routine_context": {"en": "Snack time", "es": "La merienda"},
            "selected_materials": ["video", "flashcard"],
            "group": "Group 1–2",
            "audience_type": "group",
            "child_id": "",
        }
        runtime = node_json(
            SCHOOL_ASSIGNMENT_HARNESS,
            PROTOTYPE_ROOT / "school.js",
            json.dumps(handoff),
            "?sign=more&focus=share",
        )
        initial = runtime["initialSelection"]
        self.assertEqual(initial["sign"], "more")
        self.assertEqual(initial["group"], "Group 1–2")
        self.assertEqual(initial["materials"], ["video", "flashcard"])
        self.assertTrue(initial["focused"])
        self.assertIn("prepared formats are ready to share", initial["validation"])

    def test_family_library_filters_the_same_assignment_state_and_respects_empty(self) -> None:
        harness = r'''
const fs = require("fs");
const vm = require("vm");
const storage = new Map();
const context = {
  document: { querySelector: () => null },
  window: { location: { search: "" }, matchMedia: () => ({ matches: false }) },
  __storage: storage,
  sessionStorage: {
    getItem(key) { return storage.has(key) ? storage.get(key) : null; },
    setItem(key, value) { storage.set(key, String(value)); }
  },
  URLSearchParams,
  console
};
vm.createContext(context);
const code = fs.readFileSync(process.argv[1], "utf8");
vm.runInContext(code + `
;globalThis.__familyContract = {
  snapshot(saved, pointer, requestedSign = "") {
    globalThis.__storage.clear();
    if (saved !== null) globalThis.__storage.set("kinderflowSchoolAssignments", JSON.stringify(saved));
    if (pointer) globalThis.__storage.set("kinderflowFamilyPreviewAssignmentId", JSON.stringify(pointer));
    const source = readAssignments();
    const familyContext = readFamilyContext(source.fallback, source.assignments, requestedSign);
    const visible = combineSigns(source.assignments.filter((item) => belongsToFamily(item, familyContext)));
    return { fallback: source.fallback, visible };
  }
};`, context);
const records = [
  { id: "a", signId: "more", groupId: "Group 0–1", audienceType: "group", childId: "", materials: ["video", "flashcard"] },
  { id: "b", signId: "help", groupId: "Group 1–2", audienceType: "group", childId: "", materials: ["video"] },
  { id: "c", signId: "eat", groupId: "Group 1–2", audienceType: "group", childId: "", materials: ["video", "flashcard"] },
  { id: "d", signId: "milk", groupId: "Group 1–2", audienceType: "child", childId: "Child C", materials: ["routine-card"] },
  { id: "e", signId: "water", groupId: "Group 1–2", audienceType: "child", childId: "Child D", materials: ["flashcard"] }
];
const pointer = { assignmentId: "d", groupId: "Group 1–2", audienceType: "child", childId: "Child C" };
process.stdout.write(JSON.stringify({
  absent: context.__familyContract.snapshot(null, null),
  empty: context.__familyContract.snapshot([], pointer),
  childFamily: context.__familyContract.snapshot(records, pointer),
  afterRemoval: context.__familyContract.snapshot([records[0]], pointer)
}));
'''
        runtime = node_json(harness, PROTOTYPE_ROOT / "app.js")
        self.assertTrue(runtime["absent"]["fallback"])
        self.assertEqual([item["signId"] for item in runtime["absent"]["visible"]], ["more"])
        self.assertFalse(runtime["empty"]["fallback"])
        self.assertEqual(runtime["empty"]["visible"], [])
        self.assertEqual(
            [item["signId"] for item in runtime["childFamily"]["visible"]],
            ["help", "eat", "milk"],
        )
        eat = next(item for item in runtime["childFamily"]["visible"] if item["signId"] == "eat")
        self.assertEqual(eat["materials"], ["flashcard"])
        self.assertEqual(runtime["afterRemoval"]["visible"], [])

    def test_exact_duplicate_is_blocked_but_context_changes_are_allowed(self) -> None:
        harness = r'''
const fs = require("fs");
const vm = require("vm");
const context = {
  document: { querySelector: () => null, querySelectorAll: () => [] },
  window: { location: { search: "" }, matchMedia: () => ({ matches: false }) },
  sessionStorage: { getItem: () => null, setItem() {} },
  URLSearchParams,
  Option: class {},
  console
};
vm.createContext(context);
const code = fs.readFileSync(process.argv[1], "utf8");
vm.runInContext(code + `
;globalThis.__contract = {
  assignmentKey,
  findExactDuplicate,
  availableMaterialsFor,
  replaceAssignments(value) { assignments = value; }
};`, context);
const contract = context.__contract;
const base = {
  id: "assignment-8",
  signId: "more",
  groupId: "Group 1–2",
  audienceType: "group",
  childId: "",
  materials: ["video", "flashcard", "routine-card"]
};
contract.replaceAssignments([base]);
const duplicate = { ...base, id: "", materials: ["routine-card", "video", "flashcard"] };
const differentGroup = { ...duplicate, groupId: "Group 2–3" };
const differentChild = { ...duplicate, audienceType: "child", childId: "Child C" };
const differentMaterials = { ...duplicate, materials: ["video", "flashcard"] };
process.stdout.write(JSON.stringify({
  exactDuplicate: Boolean(contract.findExactDuplicate(duplicate)),
  differentGroup: Boolean(contract.findExactDuplicate(differentGroup)),
  differentChild: Boolean(contract.findExactDuplicate(differentChild)),
  differentMaterials: Boolean(contract.findExactDuplicate(differentMaterials)),
  moreFormats: contract.availableMaterialsFor("more"),
  helpFormats: contract.availableMaterialsFor("help"),
  unknownFormats: contract.availableMaterialsFor("unknown")
}));
'''
        result = subprocess.run(
            [shutil.which("node") or "node", "-e", harness, str(PROTOTYPE_ROOT / "school.js")],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        runtime = json.loads(result.stdout)
        self.assertTrue(runtime["exactDuplicate"])
        self.assertFalse(runtime["differentGroup"])
        self.assertFalse(runtime["differentChild"])
        self.assertFalse(runtime["differentMaterials"])
        self.assertEqual(runtime["moreFormats"], ["video", "flashcard", "routine-card", "story"])
        self.assertEqual(runtime["helpFormats"], ["video", "flashcard", "routine-card"])
        self.assertEqual(runtime["unknownFormats"], [])

    def test_assignment_controls_drive_persisted_create_duplicate_edit_and_remove_flow(self) -> None:
        runtime = node_json(SCHOOL_ASSIGNMENT_HARNESS, PROTOTYPE_ROOT / "school.js")

        self.assertEqual(runtime["initialCount"], 1)
        self.assertEqual(runtime["firstShareCount"], 2)
        self.assertEqual(runtime["firstStoredCount"], 2)
        self.assertTrue(runtime["firstResultVisible"])
        self.assertEqual(runtime["toddlerAssignment"]["groupId"], "Group 1–2")
        self.assertEqual(runtime["toddlerAssignment"]["audienceType"], "group")
        self.assertEqual(
            runtime["toddlerAssignment"]["materials"],
            ["video", "flashcard", "routine-card"],
        )
        self.assertEqual(runtime["firstFamilyContext"]["assignmentId"], runtime["toddlerAssignment"]["id"])
        self.assertEqual(runtime["firstFamilyContext"]["groupId"], "Group 1–2")
        self.assertEqual(runtime["firstFamilyContext"]["audienceType"], "group")
        self.assertEqual(runtime["firstFamilyHref"], "family.html?sign=more")

        self.assertEqual(runtime["duplicateCount"], runtime["firstShareCount"])
        self.assertTrue(runtime["duplicateShown"])
        self.assertTrue(runtime["differentGroupAllowed"])
        self.assertTrue(runtime["resultVisibleBeforeDraftChange"])
        self.assertTrue(runtime["resultHiddenAfterDraftChange"])
        self.assertTrue(runtime["childShown"])
        self.assertTrue(runtime["childReset"])
        self.assertTrue(runtime["editInPlace"])

        for action, label in (("Edit", runtime["editLabel"]), ("Remove", runtime["removeLabel"])):
            self.assertTrue(label.startswith(action), label)
            self.assertIn("MORE / MÁS", label)
            self.assertIn("Preschool · 2–3", label)
            self.assertIn("Everyone in the group", label)

        self.assertTrue(runtime["removed"])
        self.assertEqual(runtime["removeCount"], 2)
        self.assertEqual(runtime["storedRemoveCount"], 2)
        self.assertTrue(runtime["storedRemoved"])

    def test_restored_assignments_filter_unsafe_and_ambiguous_ids(self) -> None:
        valid_assignment = {
            "id": "assignment-9",
            "signId": "more",
            "groupId": "Group 1–2",
            "audienceType": "group",
            "childId": "",
            "materials": ["video", "flashcard"],
        }
        restored = [
            valid_assignment,
            {**valid_assignment, "id": 1},
            {**valid_assignment, "id": "1", "signId": "help"},
            {**valid_assignment, "id": "assignment-abc", "signId": "help"},
            {
                **valid_assignment,
                "id": "assignment-9007199254740992",
                "signId": "water",
            },
            {**valid_assignment, "id": 'assignment-1"]', "signId": "eat"},
            {**valid_assignment, "signId": "help"},
            {
                **valid_assignment,
                "id": "seed-more-babies",
                "groupId": "Group 0–1",
            },
            {
                **valid_assignment,
                "id": "assignment-10",
                "audienceType": "child",
                "childId": "Child A",
            },
            {**valid_assignment, "id": "assignment-11", "materials": ["song"]},
        ]

        runtime = node_json(
            SCHOOL_RESTORE_HARNESS,
            PROTOTYPE_ROOT / "school.js",
            json.dumps(restored),
        )

        self.assertEqual(runtime["ids"], ["assignment-9", "seed-more-babies"])
        self.assertEqual(runtime["assignmentSequence"], 9)
        self.assertEqual(runtime["nextId"], "assignment-10")
        self.assertEqual(runtime["sequenceAfterNext"], 10)

        max_boundary = node_json(
            SCHOOL_RESTORE_HARNESS,
            PROTOTYPE_ROOT / "school.js",
            json.dumps([{**valid_assignment, "id": "assignment-999999999"}]),
        )
        self.assertEqual(max_boundary["ids"], ["assignment-999999999"])
        self.assertEqual(max_boundary["assignmentSequence"], 999999999)
        self.assertEqual(max_boundary["nextId"], "assignment-1")
        self.assertEqual(max_boundary["sequenceAfterNext"], 1)


if __name__ == "__main__":
    unittest.main()
