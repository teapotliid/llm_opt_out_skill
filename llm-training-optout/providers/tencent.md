# Tencent: WorkBuddy, CodeBuddy, Yuanbao (元宝)

Verified 2026-10-20. Tags: [V] official page fetched · [V-m] official text via mirror · [3P] third-party · [U] unverified.

---

## 1. WorkBuddy (Tencent Cloud desktop AI agent: workbuddy.cn / workbuddy.ai)

Desktop app on Mac/Windows, with a mobile companion. Launched 2026-03-09. Shares accounts and the `.codebuddy` config with CodeBuddy.

### Training toggle

Sources disagree on the label, so look for any of these:

| Source | Path | Label |
|---|---|---|
| Help article [V] (workbuddy.ai, 2026-06-09) | Profile avatar/name (top right) → Settings → scroll to the bottom | "Help Improve WorkBuddy" / `帮助优化模型` |
| CN privacy guide [V-m] (2026-09-22) | `设置` → `系统设置` | `体验优化计划` |
| Intl privacy policy [V] (Aug 2026) | Account name (lower left) → "System Settings" | "Experience Optimization Program" |
| CN settings doc [V] | `设置` / `功能` / `数据与安全` → `数据管理` | Shows neither label. Check `数据管理` as well. |

Switch it OFF.

**Default**
- China personal editions: ON.
- Overseas, dedicated, LearnBuddy and enterprise editions: OFF. Still verify.

**Mobile**
- The international policy says mobile has no toggle of its own and follows the desktop setting.
- The help article says mobile has avatar (top left) → Settings → bottom → "Help Improve WorkBuddy". If it's there, turn it off too.

**What it doesn't do**
- Data already in training runs stays there.
- Safety-flagged conversations may still be used for trust-and-safety models.
- Data is kept up to 14 days on servers.

**Not used for training:** when the user brings their own model API key.

**Fallback:** workbuddy_ai@tencent.com (international), codebuddy@tencent.com (CN).

### Related (optional, only on request)

- Memory: `设置` → `记忆`, and "Generate Memory" / `生成对话记忆` (on by default).
- `清除日志` (clear logs) in Settings.
- Account deletion is destructive and needs confirmation: `设置` → `账户管理` → `前往管理中心` → `账号设置` → `注销账户`. There is a 15-day cooling-off period.

---

## 2. CodeBuddy (IDE plugin, CodeBuddy IDE, CodeBuddy Code CLI)

### International / enterprise [V] (tencentcloud.com/document/product/1316/82344)

- Default: inputs/outputs are not used for training.
- If previously enabled: profile icon (top right) → "IDE Settings" → "General" → "Experience Optimization Program" → OFF.
- Inputs/outputs are still used under "legitimate interest" for R&D and troubleshooting. They are retained 14 days.

### China edition (腾讯云代码助手, codebuddy.cn)

- Agreement §9.4 [V]: the personal free edition grants a usage right over inputs/outputs for model optimization **by default**.
  - The only opt-out it gives is "通过腾讯云官网客服反馈" (send feedback through Tencent Cloud customer service).
  - This conflicts with the CN privacy statement, which says code is not used for training.
- **Agent action:**
  1. Look in IDE `设置` → `通用` for `体验优化计划` and turn it off if present [U for the CN build].
  2. Either way, prepare the written withdrawal (templates/withdrawal_request_zh.md) for acc@tencent.com or Tencent Cloud online support.

### CodeBuddy Code CLI [V] (codebuddy.ai/docs/cli/env-vars)

These env vars do NOT opt out of training. Training follows the account policy. The script sets them anyway to reduce data leaving the machine.

```
DISABLE_TELEMETRY=1
DISABLE_ERROR_REPORTING=1
DISABLE_FEEDBACK_COMMAND=1
CODEBUDDY_ARTIFACT_ENABLED=0    # disables public share links (on by default in CN)
```

---

## 3. Tencent Yuanbao (腾讯元宝)

[V-m] Privacy policy (2026-04-03) §1.10.

- `设置` → `数据管理` → `体验优化计划`: opt-in, default OFF. Verify it's off.
- `设置` → `数据管理` → `语音功能改进计划`: voice. Verify it's off.
- Team admins can lock both.
