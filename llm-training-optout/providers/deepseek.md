# DeepSeek: chat (web, iOS, Android), Open Platform API, DeepSeek Harness (`dsh`)

Verified 2026-10-20.

Verification tags:
- [V] official page fetched
- [V-code] label read from the live chat.deepseek.com web bundle's locale tables
- [V-m] official text via mirror
- [3P] third-party
- [U] unverified

---

## 1. DeepSeek chat (chat.deepseek.com, iOS, Android)

You need to sign in: logged-out chat doesn't exist.

### Required: turn off the training switch [V-code; policy V]

**Web:**
1. Left sidebar → avatar/name at the bottom (or the `⋯` next to it).
2. Open `系统设置` / `Settings`.
3. Go to the `数据管理` / `Data` tab. The tab order is General, Profile, Data, About.
4. The first row is `数据用于优化体验` / `Improve the model for everyone` → OFF.

The official CN policy path is: 点击头像区域 → 设置 → 数据管理 → 关闭"数据用于优化体验".

**Mobile:** sidebar → `⋯` by your name → Settings → **`Data controls`** (EN) / `数据管理` (ZH) → same switch → OFF. The mobile labels are unverified [3P]. If you can't find them, search Settings for "Improve the model" or "数据用于优化体验".

**How it behaves:**
- The setting is per account and server-side (`training_allowed`), so it applies across devices. Still check the app if the user uses it.
- Default is ON [3P]. Official text only says it's an opt-out.
- It covers inputs and outputs: text, voice, uploads, photos and chat history. There are no sub-switches.
- It doesn't affect data already used. For past data, use the email in step 4 below.
- It doesn't delete chats.
- It doesn't stop the network logs that law requires keeping for at least 6 months.
- It doesn't cover the API (section 2) or Harness (section 3).

### Never do while working

- Don't click `喜欢` / `不喜欢` (Like / Dislike) or open the `反馈` / Feedback modal. Feedback is used to improve quality, and the policy doesn't exclude it for users who opted out.

### Optional (ask first)

- Cookie banner: pick `仅接受必要 Cookies` / "Necessary cookies only".
- Shared links: Settings → Data → `我共享的链接` / Shared links → `管理` / Manage → delete.
- Export, then delete everything. Both are destructive, so confirm first.
  - Export: `导出所有历史对话` / Export data (the link is valid 7 days).
  - Delete: `删除所有对话` / Delete all chats.
- Delete the account (irreversible): Settings → `账号管理` / Profile → `注销账号` / Delete account.
- There's no memory or temporary-chat mode to configure.

### No toggle covers past data: send a written request

- Email privacy@deepseek.com from the account's address. EU/UK users can also cc rep_deepseek@prighter.com.
- Ask DeepSeek to exclude past conversations from training. If the user uses the API, also ask it to exclude API inputs and outputs (section 2).
- For mainland accounts, `templates/withdrawal_request_zh.md` fits.
- Draft only. The user approves before anything is sent.

---

## 2. DeepSeek Open Platform API (platform.deepseek.com, api.deepseek.com)

- **Neither the Open Platform Terms (effective 2026-04-29) nor the privacy policy says whether API data is used for training** [V]. The consumer Terms §4.3 reserves training rights and counts the API as a service.
- **No opt-out is documented.** The console returned 403 in research, so check it on screen for any data setting [U].
- **API data retention isn't documented.** The Files API supports deleting files.
- DeepSeek uses one account for the app, the Open Platform and Harness [V]. The chat switch may therefore cover API traffic, but nothing official confirms this. **Do section 1 on the same account anyway, and send the email request.**
- **Third-party harnesses** (Claude Code via `ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic`, Codex, OpenCode, WorkBuddy …) send prompts, code and tool results to DeepSeek under these same API terms. No harness-side setting changes that. Tell the user this plainly.

---

## 3. DeepSeek Harness (`dsh`, developer preview; github.com/deepseek-ai/deepseek-harness)

The Harness privacy policy (2026-09-20) [V] says session logs (inputs, uploads, outputs, tool calls) may be used to train. **The only training opt-out is by email**, to harness-privacy@deepseek.com.

Required:
1. **Session-log upload is ON by default** [V-code]. Go to Settings → `General` / `通用` → "Upload Session Log when using the official model API" / `在使用官方模型 API 时上传 Session Log` → OFF.
   - Config equivalent: plugin `session-log-deepseek` with `enabled: false`.
   - Keep it off. Turning it back on uploads the logs recorded while it was off.
2. **Feedback telemetry**: launch with `DSH_TELEMETRY_DISABLED=1`. The script writes this to the env file.
   - Without it, any `/feedback` or rating uploads the whole session to DeepSeek's collector. This happens even with custom model providers.
3. Optional: plugin `dsh-plugin-package-inventory-deepseek` → `enabled: false`. It sends your installed-plugin list with each request. No UI label was found for it.
4. Draft the training opt-out email to harness-privacy@deepseek.com. Send it only after the user approves.

With non-DeepSeek model providers, Harness says it doesn't store inputs or outputs server-side. The feedback telemetry in step 2 still applies.
