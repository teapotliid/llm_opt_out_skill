# Moonshot AI: Kimi (app and web), Kimi Code (CLI, Desktop, VS Code), Kimi Open Platform API

Verified 2026-10-20. Tags: [V] official page fetched · [3P] third-party · [U] unverified.

> **Kimi has no in-app training toggle.** Neither the China build nor the international build offers one [V: both privacy policies and the help center]. Training is ON by default, and the only opt-out is an email request. Don't search Settings for a training switch, and don't flip any similar-looking switch instead.

---

## 1. Work out which build the user has

The two builds are run by different companies, and each one has its own opt-out address.

| Build | Sites / apps | Operator | Opt-out email |
|---|---|---|---|
| China | www.kimi.com (kimi.moonshot.cn redirects here; includes the kimi.com/en English UI), Kimi CN app, PC client | 北京月之暗面科技股份有限公司 | **support@moonshot.cn** |
| International | www.kimi.ai | NOVASCENT PRIVATE LIMITED (Singapore) | **membership@moonshot.ai** |

The China build's English UI still counts as the China build.

## 2. Required: send the opt-out email (draft it, user approves, then send)

This covers all modes: chat inputs and outputs, files, images, voice, Agent / OK Computer / Deep Research, and Kimi Code on a membership login.

- **To:** the address from the table above. Send from the account's own email, or include the phone number used to log in.
- **Subject:** `申请退出模型训练 / Opt-out request: model training and improvement`
- **Body** (Chinese for the China build, English for international):

```
账号 / Account: ____ (登录手机号或邮箱 / login phone or email; 用户ID / user ID if shown: ____)

请停止将我账号下的全部内容用于模型训练、改进及研究，范围包括：对话输入与输出、上传的文件、图片与语音、
Agent / OK Computer / 深度研究任务、反馈，以及 Kimi Code 的提示词、源代码与终端输出。
请书面确认生效时间，以及历史数据是否已被排除。
（China build only: 依据《个人信息保护法》第十五条、第四十七条及 GB/T 45654—2025 第6.3条。）

Please stop using all content on my account for model training, improvement and research. This includes
chat inputs and outputs, uploaded files, images and voice, Agent / OK Computer / Deep Research tasks,
feedback, and Kimi Code prompts, source code and terminal output. Please confirm in writing when this
takes effect and whether historical data is excluded.
```

- **Expect an identity check.**
  - China build: the help page says 5–7 working days, and the policy says up to 15.
  - **Success means a confirmation email.** The UI never shows a state you can check, so report "requested, awaiting confirmation".

**What the email does not cover**
- **Past data (international):** the terms say the opt-out is prospective only and doesn't remove content already used in earlier training. The China help page says historical data is excluded.
- **Feedback:** 👍/👎 ratings and reports are licensed separately. The international licence is perpetual and irrevocable. **Never rate responses.**
- **Usage analytics and metadata** continue after the opt-out.

## 3. Optional (ask first)

- **Memory** (stated not to be used for training): the international path is `Settings` → `Personalization` → `Memory Space`. The China path is `个人主页` → `设置` → `记忆指令`. The on/off label is unverified [U].
- **Delete one chat:** `历史会话` → `删除会话`. This also disables its share links.
- **Delete the account** (irreversible): in the app, `设置` → `账号安全` → `删除账号`. On the web, `设置` → `账号设置` → `删除账号`.

---

## 4. Kimi Code (CLI `kimi`, Desktop, VS Code extension; repo MoonshotAI/kimi-code)

**Training:** with a Kimi membership login, the consumer terms apply, so training is on by default and section 2's email covers it. With an Open Platform API key, section 5 applies.

**Telemetry** (anonymous usage data; this is not a training opt-out). `scripts/optout_cli.py` handles it [V: docs and source]:

```toml
# ~/.kimi-code/config.toml   (top level; KIMI_CODE_HOME relocates the folder)
telemetry = false
# ~/.kimi-code/tui.toml
disable_feedback_survey = true
```

The env var `KIMI_DISABLE_TELEMETRY=1` goes in the script's env file. Use a current CLI, because older versions ignored this variable in `kimi -p` print mode.

- **VS Code extension:** it reads the same config and env var, and also honours VS Code's `telemetry.telemetryLevel` = `off`.
- **Desktop:** it shares `~/.kimi-code/`. That it honours `telemetry = false` is likely but unverified [U].
- **Legacy kimi-cli** (Python, archived): set `telemetry = false` in `~/.kimi/config.toml`. The script handles this too. Uninstalling it is also fine.
- **`/feedback` (alias `/bug`):** don't attach "Logs + codebase", because that uploads the codebase.

---

## 5. Kimi Open Platform API (platform.kimi.com, which platform.moonshot.cn redirects to; platform.kimi.ai, which platform.moonshot.ai redirects to)

- The sources conflict:
  - The help center says API data is **not** used for training [V].
  - The China API agreement §VI.3 grants a licence over input, output and feedback for 模型服务优化 (model service optimization) [V].
  - The international terms allow use to improve the services "unless otherwise expressly agreed in writing" [V].
- There is no dashboard setting. For a written no-training agreement, email **api-service@moonshot.ai** (international) or **support@moonshot.cn** (China). Draft the email and let the user approve it.
- Kimi Business (企业版) is stated not to train on enterprise data. Report it as "admin/contract-controlled".
