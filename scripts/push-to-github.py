#!/usr/bin/env python3
"""Push telegram-agent-kit to GitHub via API (no git push needed)."""

import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

REPO = "telegram-agent-kit"
OWNER = "0xx9"
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTHOR = {
    "name": "0xx9",
    "email": "135257896+0xx9@users.noreply.github.com",
}


def get_token() -> str:
    hosts = os.path.expanduser("~/.config/gh/hosts.yml")
    if os.path.isfile(hosts):
        for line in open(hosts):
            line = line.strip()
            if line.startswith("oauth_token:"):
                token = line.split(":", 1)[1].strip()
                if token:
                    return token
    creds_path = os.path.expanduser("~/.git-credentials")
    if os.path.isfile(creds_path):
        creds = open(creds_path).read()
        marker = f"{OWNER}:"
        if marker in creds:
            return creds.split(marker, 1)[1].split("@")[0]
    raise RuntimeError("No GitHub token found. Run: gh auth login -s repo")


def api(method, path, data=None, token="", retries=3):
    url = f"https://api.github.com{path}"
    body = None if data is None else json.dumps(data).encode()
    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
                "User-Agent": "telegram-agent-kit-push",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read().decode()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            if e.code in (409, 502, 503) and attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            err = e.read().decode()
            raise RuntimeError(f"GitHub API {e.code}: {err[:400]}") from e


def repo_exists(token):
    try:
        api("GET", f"/repos/{OWNER}/{REPO}", token=token)
        return True
    except RuntimeError as e:
        if "404" in str(e):
            return False
        raise


def create_repo(token):
    return api(
        "POST",
        "/user/repos",
        {
            "name": REPO,
            "description": "Production-ready Cursor Agent Skills for Telegram bot developers.",
            "private": False,
            "auto_init": False,
        },
        token=token,
    )


def list_files():
    out = subprocess.check_output(
        ["git", "-C", REPO_DIR, "ls-files", "-z"],
        stderr=subprocess.DEVNULL,
    )
    return [p.decode() for p in out.split(b"\0") if p]


def upload_blob(token, content: bytes):
    r = api(
        "POST",
        f"/repos/{OWNER}/{REPO}/git/blobs",
        {"content": base64.b64encode(content).decode(), "encoding": "base64"},
        token=token,
    )
    return r["sha"]


def main():
    token = get_token()
    print(f"Pushing {OWNER}/{REPO} ...")

    if not repo_exists(token):
        print("Creating repository ...")
        create_repo(token)
        time.sleep(3)
    else:
        print("Repository exists, uploading files ...")

    files = list_files()
    tree_items = []
    for path in files:
        full = os.path.join(REPO_DIR, path)
        with open(full, "rb") as f:
            blob = upload_blob(token, f.read())
        mode = "100755" if os.access(full, os.X_OK) else "100644"
        tree_items.append({"path": path, "mode": mode, "type": "blob", "sha": blob})

    tree_sha = api(
        "POST",
        f"/repos/{OWNER}/{REPO}/git/trees",
        {"tree": tree_items},
        token=token,
    )["sha"]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    author = {**AUTHOR, "date": now}
    commit_sha = api(
        "POST",
        f"/repos/{OWNER}/{REPO}/git/commits",
        {
            "message": "Initial release of Telegram Agent Kit.",
            "tree": tree_sha,
            "author": author,
            "committer": author,
        },
        token=token,
    )["sha"]

    ref_check = f"/repos/{OWNER}/{REPO}/git/ref/heads/main"
    try:
        api("GET", ref_check, token=token)
        api("PATCH", f"/repos/{OWNER}/{REPO}/git/refs/heads/main", {"sha": commit_sha, "force": True}, token=token)
    except RuntimeError:
        api(
            "POST",
            f"/repos/{OWNER}/{REPO}/git/refs",
            {"ref": "refs/heads/main", "sha": commit_sha},
            token=token,
        )

    print(f"Done: https://github.com/{OWNER}/{REPO}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(
            "\nFix: run `gh auth login -s repo` and retry, or create the repo manually on GitHub.",
            file=sys.stderr,
        )
        sys.exit(1)
