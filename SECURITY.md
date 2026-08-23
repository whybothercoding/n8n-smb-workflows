# Security Policy

## What "secure" means for this repo

This repo ships n8n workflow exports. The realistic risk here isn't a code vulnerability — it's a workflow file that got exported from a real n8n instance and still carries something instance-specific: a real credential ID, a real Slack channel ID, a real sub-workflow ID, a real database URL. `validate.sh` and CI check for this on every PR (see [How This Repo Is Tested](README.md#how-this-repo-is-tested)), but automated checks aren't infallible — pattern-based scanners don't recognize every shape of identifier as sensitive.

## Reporting a leak or vulnerability

If you spot a workflow file that contains something that looks like it came from a real, non-placeholder instance — a live API key, a real database host, a real internal ID that shouldn't be public — please:

1. **Do not open a public issue or PR containing the leaked value.**
2. Open a [private security advisory](../../security/advisories/new) on this repository, or contact the maintainer directly.
3. Include the file path and what looks wrong. No need to explain the fix — a maintainer will scrub it and, if the value could still be live (an API key, not an internal reference ID), let the affected party know so they can rotate it.

## Scope

This policy covers the workflow templates and repo tooling (`validate.sh`, `scripts/*.py`, CI). It does not cover n8n itself — report n8n platform vulnerabilities to the [n8n project](https://github.com/n8n-io/n8n/security).
