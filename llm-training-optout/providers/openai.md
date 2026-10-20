# OpenAI: ChatGPT, Codex, API platform

Verified 2026-10-20. Tags: [V] official page fetched · [V-A] official help page via Wayback snapshot (help.openai.com 403s to bots) · [3P] third-party · [U] unverified.

---

## 1. ChatGPT (web, desktop, iOS, Android)

### Required

**Turn off "Improve the model for everyone"** [V-A] (help.openai.com 7730893, 5722486)

Path:
- Web: account menu → `Settings` → `Data controls` → `Improve the model for everyone` → OFF → `Done`.
- iOS / Android: sidebar → profile icon → `Data controls` → `Improve the model for everyone` → OFF.
- Desktop app: assume the same path (`Settings` → `Data controls`) [U].

What it covers:
- Default is ON for Free, Plus and Pro.
- It applies to the whole account once signed in. When signed out it is saved per browser, so do it while signed in.
- It covers ChatGPT chats, voice transcripts, Record mode transcripts, Agent/Operator chats and screenshots, and Codex tasks on personal plans.
- It is equivalent to the Privacy Portal option "Do not train on my content" (privacy.openai.com). You only need one of them.

What it doesn't do:
- It isn't retroactive: it says "new conversations".
- It doesn't delete chats, and archiving a chat doesn't change anything.

**Verify the voice sub-toggles** [V-A] (help article 20001274)
- `Include your audio recordings` and `Include your video recordings` appear under `Data controls` only while the main toggle is ON.
- If you see them, turn them OFF first, then turn the main toggle OFF.

### Atlas browser (if installed) [V-A] (help article 12574142)

Path: blossom logo (top right) → `Settings` → `Data controls`, then:
- `Include web browsing` → OFF. This controls training on browsed content.
- `Help improve browsing & search` → OFF. These are diagnostic logs, not training, but it is ON by default.
- Optional, ask first: `Settings` → `Personalization` → `Reference browser memories`.

### Codex web [V-A] (help article 11369540)
- The ChatGPT toggle already covers Codex tasks and Computer Use screenshots.
- **"Include environments"** is a separate setting. It decides whether extra context from your Codex environments can be used for training, and neither the ChatGPT toggle nor the Privacy Portal changes it.
  - Location: Codex settings (likely chatgpt.com/codex → Settings → Data controls [U]).
  - Turn it OFF if present. If it isn't shown, report "not shown"; don't assume it is off.

### Never do while working
- Don't press 👍/👎 or "share feedback". OpenAI says: "the entire conversation associated with that feedback may be used to train our models", even after opt-out [V-A].

### Optional (only if the user asks)
- Memory: `Settings` → `Personalization` → `Memory` (and `Reference chat history` if it is shown). This is personalization, not training.
- Shared links: `Settings` → `Data controls` → shared links → manage or delete.
- Agent site logins and cookies: clear them in Data controls.
- Temporary Chat: not trained on, kept up to 30 days. Mention it to the user as an option for sensitive chats.

### Business / Enterprise / Edu
- No training by default, and admins control the setting. Report "admin-controlled". Don't change anything.

---

## 2. Codex CLI / IDE extension / ChatGPT desktop (local config)

Handled by `scripts/optout_cli.py`. It writes **user-level** `~/.codex/config.toml`, because Codex ignores `[otel]` in project config [V] (developers.openai.com/codex/config-reference):

```toml
[analytics]
enabled = false        # anonymous usage/health data; on by default

[feedback]
enabled = false        # disables /feedback log uploads (CLI, IDE ext, desktop app)

[otel]
exporter = "none"
trace_exporter = "none"
metrics_exporter = "none"   # default is "statsig"
log_user_prompt = false
```

These settings are telemetry only. Training follows the ChatGPT account setting (section 1) when signed in with ChatGPT. With an API key, the API defaults in section 3 apply.

---

## 3. OpenAI API (platform.openai.com) [V-A] (help article 10306912)

- No training by default.
- Check the organization's data-sharing settings page (likely Settings → Organization → Data controls → Sharing [U]). Make sure these are all **disabled**:
  - inputs/outputs sharing
  - eval & fine-tuning data sharing
  - Playground feedback sharing
- The "complimentary daily tokens" program means sharing is ON. Possible banners:
  - "You're enrolled for complimentary daily tokens" means the org is enrolled.
  - "You're eligible for free daily usage on traffic shared with OpenAI" means it's eligible but not necessarily enrolled.
- Leaving it ends the free tokens, which is a billing-relevant change. Confirm with the user.
- Only org Owners can change this.
