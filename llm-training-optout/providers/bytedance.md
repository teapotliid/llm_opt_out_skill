# ByteDance: Doubao (豆包), Dola, Volcano Engine Ark (Seed models), TRAE

Verified 2026-10-20. Tags:
- [V] official page fetched
- [V-m] official text read via a mirror
- [3P] third-party source
- [U] unverified

UI labels below are the strings to look for on screen. If a label is missing, search the settings panel for the keywords given, and don't guess at other toggles.

---

## 1. Doubao (豆包): app (iOS/Android), PC client, web doubao.com

Training toggle [V] (source: doubao.com/legal/model_training_faq; privacy policy §1.10(b), updated 2026-09-10)

- **Path (same on app, PC, web):** `设置` → `隐私与权限` → `帮助模型改进效果`
  - App: open `我的` (Me) first, then `设置`.
  - Web: avatar / bottom-left menu → `设置`.
  - Browser plugin: `设置` → `账户设置` → redirects to the web app. Do it there.
- **Scope:** the whole account. Changing it on one device is enough, but re-check on the others.
- **Turn OFF all four sub-switches:**
  1. `文本对话`: text and the model's replies
  2. `上传的图片、视频和文件`: uploaded images, videos, files
  3. `实时通话和语音输入的声音`: call and voice-input audio
  4. `屏幕共享和视频通话的画面`: screen-share and video-call frames (app only)
- **Default:** ON (opt-out) [3P: Tencent News 2026-09-15].
- **What it does:** content created *after* switching off is not used for model optimization.
- **What it doesn't do:**
  - It is not retroactive.
  - Feedback and reports (`点赞/点踩/反馈/举报`) are still used.

Legacy voice program [V, undated page, may be superseded]

- **Path:** `我的` → `账号设置` → `改进语音服务`. If it exists, turn it OFF.

Related (optional; only touch these if the user asked for them)

- Memory: `设置` → `记忆`
- Personalised recommendations: `设置` → `隐私与权限` → `个性化内容推荐`

Deletion (destructive: confirm with the user first)

- A single chat: open it → `删除`
- The account: `设置` → `豆包账号管理` → `删除账号`

Contact for written withdrawal: Dataprivacy@bytedance.com (reply within 15 working days).

---

## 2. Dola (ByteDance international assistant, likely ex-Cici)

[V] dola.com/legal/trainingfaq/en

- **Default:** ON.
- **Path:** account → user settings → "the relevant toggle". The label is not given on official pages [U], so search Settings for "train", "improve", "model".
- **Effect:** new conversations are not used to train.
- **Fallback:** privacy@mail.dola.com

---

## 3. Volcano Engine Ark (火山方舟) API: Doubao / Seed models

[V] Ark platform terms §3.7.7 (effective 2026-08-11)

- **Pay-as-you-go API:** no training without separate consent. Nothing to toggle.
  - Exceptions: compliance filtering, data you submit to troubleshooting tools, and abnormal-call alerts.
- **Coding Plan / Agent Plan (personal monthly subscription): grants training rights.** [V] Source: 火山引擎数据授权使用协议, 2026-08-07.
  - The grant is permanent and sublicensable, and is given via a checkbox at checkout.
  - There is no toggle. The only way out is to stop using the plan. Already-used data "技术上无法撤回" (cannot technically be withdrawn).
  - **Agent action:** report whether the user is subscribed to a Coding/Agent Plan. Cancelling a paid subscription is a billing change, so don't do it without explicit confirmation. Recommend pay-as-you-go API keys instead.
- PromptPilot has its own data-authorization agreement [U, not fetched]. Flag it if the user uses it.

---

## 4. TRAE (ByteDance AI IDE: trae.cn / trae.ai; also SOLO / TraeWork)

Privacy Mode [V] (docs.trae.cn/ide_privacy-mode)

- **IDE:** gear `设置` (top right) → left nav `账号` → `隐私模式` → switch it **ON**.
  - SOLO mode: the `设置` icon at the top right of the chat panel → `账号` → `隐私模式`.
  - International build: Settings → Account → "Privacy Mode" [U, trae.ai docs blocked].
- **Default:** OFF, so it is opt-in. A May 2026 forum post may have changed this [U].
- **With Privacy Mode off:** conversations, code snippets and AI output may be used for training. Codebase files are never used.
- **Gotcha:** Privacy Mode only works while you're signed in, and **turns off when you sign out**. Re-check after every sign-in, and tell the user.
- **The TRAE plugin for VS Code/JetBrains doesn't support Privacy Mode** [V, official forum 2026-08-13]. An earlier official answer says plugin data is not used for training.

Telemetry (separate from training) [3P: The Register 2025-07]

- Set `telemetry.telemetryLevel` to `off` in Settings (VS Code-style).
- **Tell the user this isn't a full opt-out.** Reported behavior is that other TRAE components keep sending telemetry.

TRAE CLI: no documented privacy/telemetry key found [U].
