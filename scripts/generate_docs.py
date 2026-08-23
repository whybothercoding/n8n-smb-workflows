#!/usr/bin/env python3
"""Regenerates auto-derived documentation from the workflow.json files.

Regenerates, between HTML-comment markers:
  - root README.md: the "What's Inside" and "Which Workflow Do I Need?" tables
  - each workflow's README.md: a "## Flow Diagram" Mermaid chart of `connections`

Nothing outside the marker pairs is touched. Run with --check in CI to fail
the build if committed docs are stale instead of writing them.

Usage:
  python3 scripts/generate_docs.py          # regenerate and write
  python3 scripts/generate_docs.py --check  # verify only, exit 1 if stale
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO_ROOT / "workflows"
ROOT_README = REPO_ROOT / "README.md"

CATEGORY_DISPLAY = {
    "crm": "CRM",
    "email": "Email",
    "social": "Social",
    "lead-gen": "Lead Gen",
    "reporting": "Reporting",
    "newsletter": "Newsletter",
    "utilities": "Utilities",
}

def marker_pattern(name):
    return re.compile(
        rf"<!-- {name}:START -->.*?<!-- {name}:END -->",
        re.DOTALL,
    )


TABLE_MARKER = marker_pattern("WORKFLOWS_TABLE")
PICKER_MARKER = marker_pattern("WORKFLOW_PICKER")
COUNT_BADGE_MARKER = marker_pattern("WORKFLOW_COUNT_BADGE")
FLOW_MARKER = marker_pattern("FLOW_DIAGRAM")
PICKER_COMMENT = re.compile(r"<!--\s*picker:\s*(.+?)\s*-->")

BRANCH_TYPES = {"n8n-nodes-base.if", "n8n-nodes-base.switch"}


def load_workflow(workflow_json_path):
    with open(workflow_json_path, encoding="utf-8") as f:
        data = json.load(f)
    slug_dir = workflow_json_path.parent
    category = slug_dir.parent.name
    readme_path = slug_dir / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    lines = [l for l in readme_text.splitlines() if l.strip()]
    title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("#") else data.get("name", slug_dir.name)
    one_liner = lines[1].strip() if len(lines) > 1 else ""

    picker_match = PICKER_COMMENT.search(readme_text)
    picker = picker_match.group(1) if picker_match else one_liner

    return {
        "id": data.get("id", ""),
        "name": data.get("name", ""),
        "nodes": data.get("nodes", []),
        "connections": data.get("connections", {}),
        "category": category,
        "slug": slug_dir.name,
        "rel_path": f"workflows/{category}/{slug_dir.name}/",
        "title": title,
        "one_liner": one_liner,
        "picker": picker,
        "readme_path": readme_path,
    }


def discover_workflows():
    workflows = []
    for workflow_json in WORKFLOWS_DIR.glob("*/*/workflow.json"):
        workflows.append(load_workflow(workflow_json))
    # Stable order: numeric suffix of the workflow `id` (falls back to slug).
    def sort_key(w):
        m = re.search(r"-(\d{4})-", w["id"])
        return (int(m.group(1)) if m else 9999, w["slug"])
    workflows.sort(key=sort_key)
    return workflows


def render_workflows_table(workflows):
    rows = ["| # | Workflow | Category | Description |", "|---|----------|----------|-------------|"]
    for i, w in enumerate(workflows, start=1):
        category = CATEGORY_DISPLAY.get(w["category"], w["category"].title())
        rows.append(f"| {i} | [{w['title']}]({w['rel_path']}) | {category} | {w['one_liner']} |")
    return "\n".join(rows)


def render_picker_table(workflows):
    rows = ["| If you want to… | Use |", "|---|---|"]
    for w in workflows:
        rows.append(f"| {w['picker']} | [{w['title']}]({w['rel_path']}) |")
    return "\n".join(rows)


def render_count_badge(workflows):
    n = len(workflows)
    return f"[![Workflows: {n}](https://img.shields.io/badge/workflows-{n}-blue)](#whats-inside)"


def mermaid_id(name, index):
    return f"n{index}"


def node_shape(node_id, label, node_type, is_entry_point):
    safe_label = label.replace('"', "&quot;")
    if is_entry_point:
        return f'{node_id}(["{safe_label}"])'
    if node_type in BRANCH_TYPES:
        return f'{node_id}{{"{safe_label}"}}'
    return f'{node_id}["{safe_label}"]'


def find_entry_points(nodes, connections):
    """A node with no incoming connections is a trigger/entry point, regardless of node type."""
    targets = set()
    for ports in connections.values():
        for outputs in ports.values():
            for output_targets in outputs:
                for t in output_targets:
                    targets.add(t.get("node"))
    return {n["name"] for n in nodes} - targets


def render_flow_diagram(workflow):
    nodes = workflow["nodes"]
    connections = workflow["connections"]
    name_to_id = {n["name"]: mermaid_id(n["name"], i) for i, n in enumerate(nodes)}
    entry_points = find_entry_points(nodes, connections)

    lines = ["```mermaid", "flowchart LR"]
    for n in nodes:
        node_id = name_to_id[n["name"]]
        shape = node_shape(node_id, n["name"], n.get("type", ""), n["name"] in entry_points)
        lines.append(f"    {shape}")

    for source_name, ports in connections.items():
        if source_name not in name_to_id:
            continue
        source_id = name_to_id[source_name]
        for port_type, outputs in ports.items():
            for output_targets in outputs:
                for target in output_targets:
                    target_name = target.get("node")
                    if target_name not in name_to_id:
                        continue
                    target_id = name_to_id[target_name]
                    if port_type == "main":
                        lines.append(f"    {source_id} --> {target_id}")
                    else:
                        lines.append(f"    {source_id} -. {port_type} .-> {target_id}")
    lines.append("```")
    return "\n".join(lines)


def apply_marker(text, marker_re, marker_name, body, wrap_newlines=True, error_label=None):
    if not marker_re.search(text):
        label = error_label or marker_name
        raise SystemExit(f"Missing {label} markers — cannot regenerate. Add the marker comment pair first.")
    inner = f"\n{body}\n" if wrap_newlines else body
    replacement = f"<!-- {marker_name}:START -->{inner}<!-- {marker_name}:END -->"
    return marker_re.sub(lambda m: replacement, text, count=1)


def build_targets(workflows):
    """Returns {path: new_content} for every file the generator manages."""
    targets = {}

    root_text = ROOT_README.read_text(encoding="utf-8")
    root_text = apply_marker(root_text, TABLE_MARKER, "WORKFLOWS_TABLE", render_workflows_table(workflows))
    root_text = apply_marker(root_text, PICKER_MARKER, "WORKFLOW_PICKER", render_picker_table(workflows))
    root_text = apply_marker(
        root_text, COUNT_BADGE_MARKER, "WORKFLOW_COUNT_BADGE", render_count_badge(workflows), wrap_newlines=False
    )
    targets[ROOT_README] = root_text

    for w in workflows:
        if not w["readme_path"].exists():
            continue
        text = w["readme_path"].read_text(encoding="utf-8")
        diagram = render_flow_diagram(w)
        text = apply_marker(text, FLOW_MARKER, "FLOW_DIAGRAM", diagram, error_label=f"FLOW_DIAGRAM ({w['slug']})")
        targets[w["readme_path"]] = text

    return targets


def main():
    check_only = "--check" in sys.argv
    workflows = discover_workflows()
    targets = build_targets(workflows)

    stale = []
    for path, new_content in targets.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != new_content:
            stale.append(path)
            if not check_only:
                path.write_text(new_content, encoding="utf-8")

    if check_only:
        if stale:
            print("Docs are stale. Run `python3 scripts/generate_docs.py` and commit the result:")
            for p in stale:
                print(f"  - {p.relative_to(REPO_ROOT)}")
            sys.exit(1)
        print(f"Docs are up to date ({len(workflows)} workflows).")
        return

    if stale:
        print(f"Regenerated {len(stale)} file(s):")
        for p in stale:
            print(f"  - {p.relative_to(REPO_ROOT)}")
    else:
        print(f"Already up to date ({len(workflows)} workflows).")


if __name__ == "__main__":
    main()
