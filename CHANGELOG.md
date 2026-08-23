# Changelog

All notable changes to this repository are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## 2026-08-23

### Added
- CI (`.github/workflows/ci.yml`): structural lint, generated-docs check, a real n8n-engine import check (Docker), and full-history secret scanning — nothing ran automatically before this.
- `scripts/validate.py`: full rewrite of the validation logic (one JSON parse per file instead of 12 `python3` spawns per file). Enforces every convention CLAUDE.md documents — credential placeholders, tag/category consistency, node-ID/assignment-ID/condition-ID naming, valid UUIDs, README structure and root-table sync, folder layout — not just the 6 checks the old `validate.sh` covered.
- `scripts/generate_docs.py`: generates the root README's two tables and every workflow's Mermaid `## Flow Diagram` from the actual `workflow.json` files, between marker comments. `--check` mode fails CI on drift.
- `SECURITY.md` — reporting path for a leaked credential or internal ID in a shipped template.
- `newsletter` as a declared workflow category.

### Fixed
- `workflows/newsletter/stacksignal-weekly-draft-generator.json` was invalid JSON (two unquoted literals), invisible to the old validator (wrong filename), and leaked a real Slack channel ID, a real n8n error-workflow ID, and live n8n tag records with timestamps. Rebuilt at `workflows/newsletter/stacksignal-weekly-draft-generator/` with a proper envelope, placeholders, node-ID convention, and README.
- `tags: []` on 10 of 11 existing workflows — now carries the category slug per CLAUDE.md.
- Non-UUID `versionId` values (`v1b2c3d4-...`) on all 11 existing workflows.
- Assignment-ID convention violations in `lead-capture-to-baserow` (2-part ids) and `weekly-business-digest` (4-part ids).
- Two webhook-triggered workflows (`content-repurpose-pipeline`, `support-ticket-to-slack`) had no normalizing Set node after the trigger, unlike every other webhook workflow — added one.
- CLAUDE.md's node-numbering rule said "two-digit" where every workflow in the repo uses three digits.
- CONTRIBUTING.md's README template had nested identical code fences that broke on GitHub; the root README had an orphaned H3 with no parent section.

### Removed
- `docs/superpowers/plans/` — internal AI-agent planning notes, not documentation for a public-facing repo.
