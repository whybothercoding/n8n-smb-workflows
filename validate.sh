#!/usr/bin/env bash
# Validates all workflow.json files meet repository requirements.
# Usage: bash validate.sh
# Exit 0 = all pass. Exit 1 = failures found.

set -euo pipefail

PASS=0
FAIL=0
ERRORS=()

check_workflow() {
  local file="$1"
  local errs=0

  # 1. Valid JSON
  if ! python3 -m json.tool "$file" > /dev/null 2>&1; then
    ERRORS+=("$file: invalid JSON")
    ((errs++))
  fi

  # 2. Required top-level fields
  for field in id name nodes connections active settings versionId; do
    if ! python3 -c "
import json, sys
d = json.load(open('$file'))
assert '$field' in d, '$field missing'
" 2>/dev/null; then
      ERRORS+=("$file: missing required field '$field'")
      ((errs++))
    fi
  done

  # 3. active must be false
  if ! python3 -c "
import json, sys
d = json.load(open('$file'))
assert d.get('active') is False
" 2>/dev/null; then
    ERRORS+=("$file: 'active' must be false")
    ((errs++))
  fi

  # 4. executionOrder must be "v1"
  if ! python3 -c "
import json, sys
d = json.load(open('$file'))
assert d.get('settings', {}).get('executionOrder') == 'v1'
" 2>/dev/null; then
    ERRORS+=("$file: settings.executionOrder must be 'v1'")
    ((errs++))
  fi

  # 5. errorWorkflow must be present in settings
  if ! python3 -c "
import json, sys
d = json.load(open('$file'))
assert 'errorWorkflow' in d.get('settings', {})
" 2>/dev/null; then
    ERRORS+=("$file: settings.errorWorkflow is missing")
    ((errs++))
  fi

  # 6. No raw API tokens in HTTP header values (must use REPLACE_WITH_ prefix)
  local bad_tokens
  bad_tokens=$(python3 -c "
import json, re
d = json.load(open('$file'))
text = json.dumps(d)
matches = re.findall(r'(?:Token|Bearer)\s+([A-Za-z0-9_]+)', text)
bad = [m for m in matches if not m.upper().startswith('REPLACE_WITH')]
print('\n'.join(bad))
" 2>/dev/null)
  if [ -n "$bad_tokens" ]; then
    ERRORS+=("$file: hardcoded token found in header — use REPLACE_WITH_... placeholder")
    ((errs++))
  fi

  if [ "$errs" -eq 0 ]; then
    ((PASS++))
    echo "  ✓ $file"
  else
    ((FAIL++))
    echo "  ✗ $file  ($errs issue(s))"
  fi
}

echo "=== n8n workflow validation ==="
echo ""

while IFS= read -r -d '' file; do
  check_workflow "$file"
done < <(find workflows -name "workflow.json" -print0 | sort -z)

echo ""
echo "Results: $PASS passed, $FAIL failed"
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo "Issues:"
  for err in "${ERRORS[@]}"; do
    echo "  - $err"
  done
  exit 1
fi

echo "All workflows valid."
