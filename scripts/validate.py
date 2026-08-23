#!/usr/bin/env python3
"""Validates every workflow.json + README.md pair against the conventions
documented in CLAUDE.md. One JSON parse per file (unlike the old bash+python
validator, which spawned ~12 Python interpreters per file).

Usage:
  python3 scripts/validate.py         # human-readable, exit 0/1
  python3 scripts/validate.py --json  # machine-readable summary on stdout
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO_ROOT / "workflows"
ROOT_README = REPO_ROOT / "README.md"

VALID_CATEGORIES = {"crm", "email", "social", "lead-gen", "reporting", "newsletter", "utilities"}
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)
WORKFLOW_NUM_RE = re.compile(r"-(\d{4})-")
NODE_ID_RE = re.compile(r"^node-(\d{3})-[a-z0-9-]+$")
ASSIGN_ID_RE = re.compile(r"^assign-(\d{3})-\d{3}$")
COND_ID_RE = re.compile(r"^cond-(\d{3})-\d{3}$")
REQUIRED_ENVELOPE = {
    "id", "meta", "name", "nodes", "connections", "pinData",
    "active", "settings", "staticData", "tags", "versionId",
}
REQUIRED_README_SECTIONS = [
    "## Use Case",
    "## Required Credentials",
    "## Node Overview",
    "## Flow Diagram",
    "## Configuration",
    "## Example",
]
# Secrets pasted directly into header/body values instead of a REPLACE_WITH_ placeholder.
SECRET_PATTERNS = [
    re.compile(r"(?:Token|Bearer)\s+([A-Za-z0-9_\-./+=]{8,})"),
    re.compile(r"\b(sk-[A-Za-z0-9]{16,})\b"),
    re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{20,})\b"),
    re.compile(r"\b(xox[baprs]-[A-Za-z0-9-]{10,})\b"),
]


def fail(errors, msg):
    errors.append(msg)


def check_envelope(data, errors):
    missing = REQUIRED_ENVELOPE - data.keys()
    if missing:
        fail(errors, f"missing required top-level field(s): {sorted(missing)}")

    if data.get("active") is not False:
        fail(errors, "'active' must be false")

    settings = data.get("settings", {})
    if settings.get("executionOrder") != "v1":
        fail(errors, "settings.executionOrder must be 'v1'")

    if data.get("pinData") != {}:
        fail(errors, "pinData must be {}")
    if data.get("staticData") is not None:
        fail(errors, "staticData must be null")

    meta = data.get("meta", {})
    if not isinstance(meta, dict) or meta.get("instanceId") != "":
        fail(errors, "meta.instanceId must be an empty string")

    for field, pattern_name in (("id", "id"), ("versionId", "versionId")):
        val = data.get(field, "")
        if not UUID_RE.match(val or ""):
            fail(errors, f"'{pattern_name}' is not a valid UUID: {val!r}")


def check_error_workflow(data, category, errors):
    settings = data.get("settings", {})
    ew = settings.get("errorWorkflow")
    if ew is None:
        fail(errors, "settings.errorWorkflow is missing")
        return
    if category == "utilities":
        if ew not in ("", "REPLACE_WITH_YOUR_ERROR_WORKFLOW_ID"):
            fail(errors, f"utilities workflow's errorWorkflow should be '' or the placeholder, got {ew!r}")
    elif ew != "REPLACE_WITH_YOUR_ERROR_WORKFLOW_ID":
        fail(errors, f"settings.errorWorkflow must be the placeholder, got {ew!r}")


def check_tags(data, category, errors):
    tags = data.get("tags")
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        fail(errors, "tags must be an array of plain strings (not n8n tag-record objects)")
        return
    if category not in tags:
        fail(errors, f"tags must include the category slug {category!r}, got {tags}")


def check_credentials(nodes, errors):
    for node in nodes:
        creds = node.get("credentials")
        if not creds:
            continue
        for cred_type, cred in creds.items():
            cred_id = cred.get("id")
            if cred_id != "REPLACE_WITH_YOUR_CREDENTIAL_ID":
                fail(
                    errors,
                    f"node {node.get('name')!r} credential '{cred_type}' id must be "
                    f"REPLACE_WITH_YOUR_CREDENTIAL_ID, got {cred_id!r}",
                )


def check_secrets(data, errors):
    text = json.dumps(data)
    seen = set()
    for pattern in SECRET_PATTERNS:
        for match in pattern.findall(text):
            if match.upper().startswith("REPLACE_WITH") or match in seen:
                continue
            seen.add(match)
            fail(errors, f"possible hardcoded secret in workflow body: {match[:12]}...")


def check_node_ids(nodes, workflow_num, errors):
    seen_ids = set()
    for node in nodes:
        node_id = node.get("id", "")
        if node_id in seen_ids:
            fail(errors, f"duplicate node id: {node_id!r}")
        seen_ids.add(node_id)

        m = NODE_ID_RE.match(node_id)
        if not m:
            fail(errors, f"node {node.get('name')!r} id {node_id!r} doesn't match node-{{NNN}}-{{purpose}}")
        elif workflow_num and m.group(1) != workflow_num:
            fail(errors, f"node {node.get('name')!r} id {node_id!r} workflow number doesn't match this file's ({workflow_num})")

        params = node.get("parameters", {})
        assignments = params.get("assignments", {}).get("assignments", [])
        for a in assignments:
            a_id = a.get("id", "")
            m2 = ASSIGN_ID_RE.match(a_id)
            if not m2:
                fail(errors, f"node {node.get('name')!r} assignment id {a_id!r} doesn't match assign-{{NNN}}-{{seq}}")
            elif workflow_num and m2.group(1) != workflow_num:
                fail(errors, f"node {node.get('name')!r} assignment id {a_id!r} workflow number mismatch")

        conditions = params.get("conditions", {}).get("conditions", [])
        for c in conditions:
            c_id = c.get("id", "")
            m3 = COND_ID_RE.match(c_id)
            if not m3:
                fail(errors, f"node {node.get('name')!r} condition id {c_id!r} doesn't match cond-{{NNN}}-{{seq}}")
            elif workflow_num and m3.group(1) != workflow_num:
                fail(errors, f"node {node.get('name')!r} condition id {c_id!r} workflow number mismatch")


def check_connections(nodes, connections, errors):
    node_names = {n["name"] for n in nodes}
    for source, ports in connections.items():
        if source not in node_names:
            fail(errors, f"connections references unknown source node {source!r}")
        for outputs in ports.values():
            for targets in outputs:
                for t in targets:
                    if t.get("node") not in node_names:
                        fail(errors, f"connections references unknown target node {t.get('node')!r}")


def check_readme(readme_path, node_overview_expected, errors):
    if not readme_path.exists():
        fail(errors, "README.md is missing")
        return
    text = readme_path.read_text(encoding="utf-8")
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines or not lines[0].startswith("# "):
        fail(errors, "README.md must start with an H1 title")

    positions = []
    for section in REQUIRED_README_SECTIONS:
        idx = text.find(f"\n{section}\n") if not text.startswith(section) else 0
        if idx == -1:
            fail(errors, f"README.md missing required section {section!r}")
        positions.append(idx)
    if all(p != -1 for p in positions) and positions != sorted(positions):
        fail(errors, "README.md sections are out of order")

    for node in node_overview_expected:
        name, ntype = node["name"], node.get("type", "")
        if f"| {name} |" not in text or f"`{ntype}`" not in text:
            fail(errors, f"Node Overview table missing/mismatched row for node {name!r} ({ntype})")


def check_root_readme_row(rel_path, root_readme_text, errors):
    if f"]({rel_path})" not in root_readme_text:
        fail(errors, f"root README.md 'What's Inside' table has no row linking to {rel_path}")


def validate_workflow(workflow_json_path, root_readme_text):
    errors = []
    try:
        data = json.loads(workflow_json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"invalid JSON: {e}"]

    slug_dir = workflow_json_path.parent
    category = slug_dir.parent.name
    rel_path = f"workflows/{category}/{slug_dir.name}/"

    if category not in VALID_CATEGORIES:
        fail(errors, f"category {category!r} is not declared in CLAUDE.md's category list")

    check_envelope(data, errors)
    check_error_workflow(data, category, errors)
    check_tags(data, category, errors)

    nodes = data.get("nodes", [])
    connections = data.get("connections", {})
    check_credentials(nodes, errors)
    check_secrets(data, errors)
    check_connections(nodes, connections, errors)

    m = WORKFLOW_NUM_RE.search(data.get("id", ""))
    workflow_num = m.group(1)[-3:] if m else None  # node IDs use the 3-digit form (0001 -> 001)
    check_node_ids(nodes, workflow_num, errors)

    check_readme(slug_dir / "README.md", nodes, errors)
    check_root_readme_row(rel_path, root_readme_text, errors)

    other_files = {p.name for p in slug_dir.iterdir()} - {"workflow.json", "README.md"}
    if other_files:
        fail(errors, f"unexpected files in workflow folder: {sorted(other_files)}")

    return errors


def find_stray_json(errors_by_file):
    """Flags any *.json under workflows/ that isn't at <category>/<slug>/workflow.json."""
    for json_path in WORKFLOWS_DIR.rglob("*.json"):
        rel_parts = json_path.relative_to(WORKFLOWS_DIR).parts
        is_well_formed = len(rel_parts) == 3 and rel_parts[-1] == "workflow.json"
        if not is_well_formed:
            errors_by_file[json_path] = [
                "stray JSON file — must live at workflows/<category>/<slug>/workflow.json"
            ]


def main():
    as_json = "--json" in sys.argv
    root_readme_text = ROOT_README.read_text(encoding="utf-8") if ROOT_README.exists() else ""

    results = {}
    for workflow_json in sorted(WORKFLOWS_DIR.glob("*/*/workflow.json")):
        results[workflow_json] = validate_workflow(workflow_json, root_readme_text)
    find_stray_json(results)

    if not results:
        print("No workflow.json files found.")
        sys.exit(1)

    passed = sum(1 for e in results.values() if not e)
    failed = len(results) - passed

    if as_json:
        print(json.dumps(
            {str(p.relative_to(REPO_ROOT)): e for p, e in sorted(results.items())},
            indent=2,
        ))
        sys.exit(1 if failed else 0)

    print("=== n8n workflow validation ===\n")
    for path, errors in sorted(results.items()):
        rel = path.relative_to(REPO_ROOT)
        if errors:
            print(f"  ✗ {rel}")
            for e in errors:
                print(f"      - {e}")
        else:
            print(f"  ✓ {rel}")

    print(f"\nResults: {passed} passed, {failed} failed\n")
    if failed:
        sys.exit(1)
    print("All workflows valid.")


if __name__ == "__main__":
    main()
