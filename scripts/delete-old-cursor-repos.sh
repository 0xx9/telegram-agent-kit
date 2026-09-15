#!/usr/bin/env bash
# Delete leftover backup repos created by push_clean_github.py (*-old-cursor-*)
set -euo pipefail

echo "Checking GitHub auth (needs delete_repo scope)..."
if ! gh auth status >/dev/null 2>&1; then
  echo "Run: gh auth login -h github.com -s repo,delete_repo"
  exit 1
fi

mapfile -t repos < <(gh repo list 0xx9 --limit 200 --json name --jq '.[].name' | grep 'old-cursor' || true)

if [ "${#repos[@]}" -eq 0 ]; then
  echo "No old-cursor repos found. Done."
  exit 0
fi

echo "Will delete ${#repos[@]} repos:"
printf '  - %s\n' "${repos[@]}"
echo

for repo in "${repos[@]}"; do
  echo "Deleting 0xx9/$repo ..."
  gh repo delete "0xx9/$repo" --confirm
done

echo
echo "Done. Remaining:"
gh repo list 0xx9 --limit 200 --json name --jq '.[].name' | grep 'old-cursor' || echo "  (none)"
