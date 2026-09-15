# Publish checklist

Your GitHub token is missing **`repo`** scope, so auto-create failed. Do this once:

## Step 1 — Refresh GitHub login (2 minutes)

In terminal:

```bash
gh auth refresh -h github.com -s repo
```

Or create a new token at https://github.com/settings/tokens with **`repo`** scope, then:

```bash
gh auth login -h github.com
```

## Step 2 — Create empty repo

Open: https://github.com/new

- **Name:** `telegram-agent-kit`
- **Public**
- Do **not** add README (we already have one)

## Step 3 — Push

```bash
cd /root/telegram-agent-kit
python3 scripts/push-to-github.py --existing
```

Or with git:

```bash
gh auth setup-git
git remote set-url origin https://github.com/0xx9/telegram-agent-kit.git
git push -u origin main
```

## Step 4 — Add topics (helps discovery)

On GitHub repo page → ⚙️ → Topics:

```
telegram, telegram-bot, cursor, cursor-skills, aiogram, telethon, agent-skills, developer-tools
```

## Step 5 — Pin repo on your profile

GitHub profile → Customize → Pin `telegram-agent-kit`

## Step 6 — First post

Copy text from [SOCIAL.md](SOCIAL.md) → post in r/TelegramBots or aiogram chat.

---

Full growth plan: [GROWTH.md](GROWTH.md)
