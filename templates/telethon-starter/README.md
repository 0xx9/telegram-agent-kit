# Telethon starter

Minimal Telethon client with env config and flood-wait handling.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add API_ID and API_HASH from https://my.telegram.org
python client.py
```

First run prompts for phone login interactively. Session saved locally — never commit it.

## Env

| Variable | Required | Description |
|----------|----------|-------------|
| `API_ID` | yes | From my.telegram.org |
| `API_HASH` | yes | From my.telegram.org |
| `SESSION_NAME` | no | Session file name (default: user) |
