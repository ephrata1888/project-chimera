#!/bin/sh
set -eu

# Spec-check script: prefer .github/copilot-instructions.md (repo now uses that),


TARGET=".github/copilot-instructions.md"

echo "Running spec check against $TARGET" >&2

grep -q 'Project Context: "This is Project Chimera, an autonomous influencer system."' "$TARGET" || { echo "$TARGET missing Project Context line" >&2; exit 2; }
grep -q 'The Prime Directive: "NEVER generate code without checking specs/ first."' "$TARGET" || { echo "$TARGET missing Prime Directive line" >&2; exit 2; }

echo "Spec check: $TARGET contains required lines"
exit 0
