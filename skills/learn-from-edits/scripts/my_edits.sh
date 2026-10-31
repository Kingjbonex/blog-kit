#!/usr/bin/env bash
# Show the author's own edits to a file: a word diff of each commit they authored that touched it.
# Usage: my_edits.sh <file> "<author name or email pattern>"
set -euo pipefail
file="${1:?usage: my_edits.sh <file> <author-pattern>}"
author="${2:?usage: my_edits.sh <file> <author-pattern>}"
for sha in $(git log --author="$author" --format=%h -- "$file"); do
  echo "=== $(git log -1 --format='%h %ad %s' --date=short "$sha")"
  git show "$sha" --word-diff=plain --format= -- "$file"
done
