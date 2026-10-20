---
name: llm-training-optout
description: Turn off model-training / data-sharing settings on the user's own AI accounts and local agent CLIs. Covers ChatGPT, Codex, Claude, Claude Code, Gemini, Gemini CLI, Antigravity, Grok/X, Grok Build, Meta AI / Muse Spark / Muse (incl. Meta AI in WhatsApp, Instagram, Facebook, AI glasses), Doubao (豆包), Volcano Ark (Seed), TRAE, WorkBuddy, CodeBuddy, Yuanbao, Kimi / Kimi Code and DeepSeek / DeepSeek Harness. Use when the user asks to opt out of AI training, stop data sharing, "make sure X doesn't train on my chats", or audit privacy settings across AI tools. Drives web/app settings via computer use and patches local CLI config via a script.
---

# LLM training opt-out

Turn off "use my data to train models" on accounts the user owns, then report exactly what changed. This skill has two halves:

1. **Local harnesses** (Claude Code, Codex CLI, Gemini CLI, Kimi Code, CodeBuddy Code, DeepSeek Harness, Meta Muse Code). Run `scripts/optout_cli.py`. It edits config files, backs each one up first, and is idempotent.
2. **Account settings** (web/desktop/mobile). Drive the settings UI with computer use, following `providers/<vendor>.md`.

Most training opt-outs are **account-level** settings stored server-side. CLI flags mostly control telemetry, not training. You need both halves.

## Ground rules (read before acting)

- **Only the user's own accounts.** Only on a device the user is operating, with the user already signed in.
  - Never type passwords, 2FA codes or recovery codes.
  - Never solve CAPTCHAs.
  - If a login, re-auth or CAPTCHA wall appears, stop and ask the user to complete it.
- **Only switch training/data-sharing settings OFF**, plus the specific related toggles listed as "required" in the provider file. Anything listed as optional needs the user's say-so:
  - memory
  - chat history
  - personalization
  - connectors
- **Destructive or billing actions need explicit confirmation in this conversation.** That includes:
  - deleting chats or accounts
  - cancelling subscriptions (e.g., Volcano Ark Coding Plan)
  - sending emails or forms on the user's behalf
  - Show what will happen, then wait.
- **Never press feedback buttons** (👍/👎, "report", "share feedback") while working. On several providers, feedback makes that conversation trainable regardless of the toggle.
- **Labels drift.** Provider files give the label strings verified on 2026-10-20.
  - If a label isn't found, search the settings panel for these keywords:
    - English: "train", "improve", "model", "data controls", "privacy", "activity"
    - Chinese: `训练`, `改进`, `优化`, `体验优化计划`, `隐私`, `数据管理`
  - Read the toggle's description before flipping it.
  - If it's still ambiguous, ask the user. Don't flip guesses.
- **Verify every change.** Reload the page, re-open the setting and confirm the OFF state. Take a screenshot if your harness supports it.
- **Your own provider sees this.** As a computer-use agent, your screenshots and actions go to whoever runs you. Tell the user once at the start that this session may itself be logged by the agent's provider.

## Quick reference: the main training switch per product

Exact strings, verified 2026-10-20. The provider files cover the extra toggles, caveats and fallbacks.

| Product | Where | Switch → state |
|---|---|---|
| ChatGPT (all platforms) | Settings → Data controls | "Improve the model for everyone" → OFF |
| Codex web | Codex settings | "Include environments" → OFF (separate from the ChatGPT toggle) |
| Claude / Claude Code (Free/Pro/Max) | claude.ai/settings/data-privacy-controls | "Help Improve our AI models" → OFF |
| Gemini app | myactivity.google.com/product/gemini | Keep Activity → Turn off |
| Antigravity | Settings → Account (CLI: `/config`) | "Enable Telemetry" → OFF |
| Grok | Settings → Data Controls (web: Data) | "Improve the Model" → OFF |
| Grok on X | Privacy & Safety → Data sharing and personalization → Grok & Third-party Collaborators | "Allow your public data … used for training and fine-tuning" → untick |
| Grok Build | `/privacy` | code-data retention → OFF |
| Doubao 豆包 | 设置 → 隐私与权限 | 帮助模型改进效果 → all 4 sub-switches OFF |
| TRAE | 设置 → 账号 | 隐私模式 / Privacy Mode → **ON** (resets on sign-out) |
| WorkBuddy | Settings (bottom) or 设置 → 系统设置 | "Help Improve WorkBuddy" / 帮助优化模型 / 体验优化计划 → OFF |
| CodeBuddy | IDE Settings → General | "Experience Optimization Program" / 体验优化计划 → OFF; CN free edition also needs a written withdrawal |
| Yuanbao 元宝 | 设置 → 数据管理 | 体验优化计划, 语音功能改进计划 → OFF |
| Volcano Ark API | — | No training by default; the **Coding/Agent Plan** grants permanent training rights, and the only way out is to stop using the plan |
| Meta AI (app, meta.ai, WhatsApp, IG, FB, Messenger; runs Muse Spark) | **No toggle in the US or most regions** | EU/UK and some other countries: objection forms (`providers/meta.md` §4). Elsewhere: cleanup only (delete chats, `/reset-ai`); never tap Share/Post |
| Muse agent (muse.ai) | Settings → Data controls | "Help improve our AI models" → OFF (also covers past interactions) |
| Meta AI glasses | Meta AI app → glasses Settings → Experiences → Meta AI; and Glasses privacy | "Store visual data from AI experiences" → OFF; Cloud media → OFF; voice storage can't be turned off in the US, CA, AU or SG (delete only) |
| Meta Muse Code (`muse`) | `/settings` (needs ≥ 1.4.8) | Contributor mode → OFF (subscriptions default ON); API keys: avoid `-contributor` model IDs |
| Kimi (kimi.com / kimi.ai) | **No toggle exists**; default ON | Email opt-out: support@moonshot.cn (China build, incl. kimi.com/en) or membership@moonshot.ai (kimi.ai); also covers Kimi Code on a membership login |
| Kimi Code | `~/.kimi-code/config.toml` (script) | `telemetry = false`; this is telemetry only, training needs the email |
| DeepSeek chat | avatar → 系统设置/Settings → 数据管理/Data (mobile: Data controls) | 数据用于优化体验 / "Improve the model for everyone" → OFF |
| DeepSeek API | — | Training terms unclear, no opt-out documented: do the chat switch on the same account, then draft an email to privacy@deepseek.com |
| DeepSeek Harness (`dsh`) | Settings → General | "Upload Session Log when using the official model API" → OFF; `DSH_TELEMETRY_DISABLED=1`; training opt-out only by email |

## Workflow

1. **Scope.** Ask which products and accounts the user has, unless they said "all". For each, note:
   - the plan tier: consumer/free/paid vs business/enterprise/API (enterprise is usually admin-controlled and no-training by default)
   - the region (China vs international builds differ)
2. **Local CLIs first.** These are fast and need no login.
   ```bash
   python3 scripts/optout_cli.py --dry-run   # show planned edits
   python3 scripts/optout_cli.py             # apply (backs up each file to *.bak-optout-<timestamp>)
   python3 scripts/optout_cli.py --check     # report current state only
   python3 scripts/optout_cli.py --only dsh  # force a tool that isn't auto-detected (e.g. Harness run via npx)
   ```
   The script only touches tools whose config dir exists, unless you pass `--create`. Shell-profile env vars are written to a separate file that the user sources, so it never edits `.bashrc` silently. Read the script's summary and pass it on.
3. **Account settings.** For each in-scope product, open `providers/<vendor>.md` and follow its steps. Do every surface the file lists: web, desktop, mobile, plus any separate toggles for voice, video or browsing.
   | Vendor file | Products |
   |---|---|
   | `providers/openai.md` | ChatGPT (web/desktop/mobile, voice, Atlas/agent), Codex (cloud, CLI, IDE), OpenAI API platform |
   | `providers/anthropic.md` | Claude (claude.ai web/desktop/mobile, Claude in Chrome), Claude Code, Anthropic API / Console |
   | `providers/google.md` | Gemini app (web/Android/iOS), Gemini CLI, Antigravity (replaced free Code Assist on 2026-06-18), AI Studio / Gemini API, Jules |
   | `providers/xai.md` | Grok (grok.com, apps), Grok inside X, xAI API, Grok Build CLI |
   | `providers/bytedance.md` | Doubao 豆包, Dola, Volcano Ark (Seed models), TRAE / SOLO |
   | `providers/tencent.md` | WorkBuddy, CodeBuddy (IDE/CLI), Yuanbao 元宝 |
   | `providers/meta.md` | Muse Spark (model), Meta AI app / meta.ai, Meta AI in WhatsApp / Instagram / Facebook / Messenger, Muse agent app, Vibes, EU/UK objection forms, AI glasses, Meta Model API / Muse Code |
   | `providers/kimi.md` | Kimi app/web (China kimi.com and international kimi.ai builds), Kimi Code (CLI/Desktop/VS Code), Kimi Open Platform API |
   | `providers/deepseek.md` | DeepSeek chat (web/iOS/Android), Open Platform API, DeepSeek Harness (`dsh`) |
4. **No toggle, or terms say "contact us".** Draft a written request. Show the draft to the user, and send it only on their explicit go-ahead.
   - China products: `templates/withdrawal_request_zh.md` (PIPL Art. 15/47, GB/T 45654-2025 §6.3)
   - Elsewhere: the provider's privacy-request portal or email listed in its file
5. **Report.** Produce a table with one row per product × surface:
   - state before → after
   - how verified (reloaded / screenshot / script check)
   - remaining caveats

   Always include these caveats:
   - **Not retroactive.** Opt-outs stop *future* training. Past data may already be in trained models. Deletion is a separate, destructive step.
   - **Retention ≠ training.** Opted-out data can still be stored for safety review, abuse monitoring or legal holds.
   - **Re-check triggers.** Re-run after:
     - signing out and back in (TRAE Privacy Mode resets)
     - new devices
     - new products
     - terms updates
   - **Feedback overrides.** Avoid rating responses on providers where feedback is trainable.

## What this skill cannot do

- It can't change admin-locked enterprise or Workspace settings. Tell the user to ask their admin.
- It can't prove the provider honours the setting. See `../../REPORT.md` §4 on detection limits.
- It can't recover data already used for training.
