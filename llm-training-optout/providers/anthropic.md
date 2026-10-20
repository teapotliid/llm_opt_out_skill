# Anthropic: Claude apps, Claude Code, Console/API

Verified 2026-10-20. Tags: [V] official page fetched · [3P] third-party · [U] unverified.

---

## 1. Claude (claude.ai web, desktop, iOS/Android) — Free, Pro, Max

### Required

**Turn off "Help Improve our AI models"** [V] (privacy.claude.com article 12109829, 2026-08-03)

- Deep link: https://claude.ai/settings/data-privacy-controls
- Path: your name (settings menu) → `Settings` → `Privacy` → under "Help Improve our AI models", toggle it OFF. On mobile, tap your name directly.
- Help articles call this setting "Model Improvement".
- Covers new chats *and Claude Code sessions* from this account.
- Retention: 30 days when off, 5 years when on.
- Not retroactive for training runs that have already started. Flagged conversations may still train trust-and-safety models.
- Default: not stated officially [U]. Always check.

### Never do while working

Don't rate responses (👍/👎). Feedback stores the whole conversation for 5 years and can be used for training regardless of the toggle [V].

### Optional (only if the user asks)

- Memory: `Settings` → `Memory`. Toggles there are "Generate memory from chats", "Search and reference chats" and "Include sensitive topics in memory". Memory is personalization, not training.
- `Settings` → `Privacy` → Location metadata (OFF), and Shared chats → `Manage` [3P].
- Incognito chats (ghost icon) are never used for training, even with Model Improvement on. Mention this as an option for sensitive work.
- Claude in Chrome has no separate training toggle; it follows the account setting [U].

### Team / Enterprise / Edu / Gov

No training by default [V]. Report "admin-controlled". Owners can disable member feedback via `Organization settings` → `Data and Privacy` → "Rate chats".

---

## 2. Claude Code

### Training

It follows the claude.ai account setting above for Free/Pro/Max logins. Pro/Max users can also run `/privacy-settings` inside Claude Code [V]. API-key, Bedrock and Vertex usage is not trained on by default.

### Local config (handled by `scripts/optout_cli.py`)

The script merges these into the `env` block of user-level `~/.claude/settings.json` [V] (code.claude.com/docs env-vars and settings):

```json
{
  "env": {
    "DISABLE_TELEMETRY": "1",
    "DISABLE_ERROR_REPORTING": "1",
    "DISABLE_FEEDBACK_COMMAND": "1",
    "CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY": "1"
  },
  "feedbackSurveyRate": 0
}
```

| Setting | Effect |
|---|---|
| `DISABLE_TELEMETRY` | Usage metrics off. These never contained code or prompts. This also disables feature flags, so Remote Control stops working. |
| `DISABLE_ERROR_REPORTING` | Stack-trace reports off. They are on by default for Pro/Max. |
| `DISABLE_FEEDBACK_COMMAND` | Disables `/feedback`, `/bug` and `/share`. Transcripts sent through these are kept 5 years. |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` and `feedbackSurveyRate: 0` | Session survey and its transcript-share follow-up off. |

Optional, behind `--strict`: `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`. This also disables auto-updates and release notes, so the user must update manually.

All of these are telemetry and feedback channels. None of them is the training switch; that's the account toggle in section 1.

---

## 3. Claude Console / API (platform.claude.com)

- No training by default.
- Check the **Development Partner Program**: Console → `Data retention` page (platform.claude.com/settings/privacy) → "Usage data and feedback" [V]. If it shows **Leave**, the org is enrolled.
  - Leaving is an org-level change. Confirm with the user (an admin) first.
  - Data already shared is kept for 2 years after leaving.
