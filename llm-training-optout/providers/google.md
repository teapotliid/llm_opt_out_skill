# Google: Gemini app, Gemini CLI, Antigravity, Gemini API / AI Studio

Verified 2026-10-20. Verification tags used below:
- [V] official page fetched
- [S] search summary only
- [U] unverified

> On 2026-06-18 Google shut down the free Gemini Code Assist IDE extension and Gemini CLI "Login with Google" for unpaid, AI Pro and Ultra users. The replacement is **Antigravity** (see section 3) [V].

---

## 1. Gemini app (gemini.google.com, Android, iOS)

### Required: turn off Keep Activity [V]

- Deep link: https://myactivity.google.com/product/gemini
- Web: gemini.google.com → `Settings & help` → `Activity` → the `On` control → `Turn off`. The other choice, `Turn off and delete activity`, also deletes history, so confirm with the user before picking it.
- Android / iOS: `Menu` → profile picture or initial → `Gemini Apps Activity` → same choices as on web.
- Older UI name: "Gemini Apps Activity". Current name: "Keep Activity".
- Default: ON for users 18 and over.
- Off does not mean nothing is stored:
  - Chats are still kept up to **72 hours**.
  - Chats already picked for **human review are kept up to 3 years**, separately, and turning the setting off does not delete them.
  - Past activity is not deleted unless the user picks the delete option.
- Covers Gemini in Chrome as well.
- Work and school accounts are admin-controlled. Report this rather than changing anything.

### Audio, Live video and screenshare [V]

- Checkbox: "Improve Google services with your audio and Gemini Live videos & screenshares". Off by default.
- It only shows while Keep Activity is ON. If it's visible, untick it first, then turn Keep Activity off.
- **Don't turn Keep Activity on just to reach this checkbox.**

### Never do while working

- Don't send feedback (thumbs up/down or "report"). Feedback is used even after opting out and is kept for 3 years.

### Optional (ask first)

- Memory: `Settings & help` → `Personal context` → `Memory`. This is personalization, not training.
- If the user wants to delete past activity:
  - Use `myactivity.google.com/product/gemini` → Delete.
  - Setting auto-delete to 3 months shortens retention. The default is 18 months.

### Not covered

- Gemini Notebook (formerly NotebookLM) has no toggle. Its content is not used for training unless the user sends feedback [V].

---

## 2. Gemini CLI (still used with an API key, Vertex, or an org account)

`scripts/optout_cli.py` writes these to `~/.gemini/settings.json` [V] (gemini-cli docs):

```json
{
  "privacy": { "usageStatisticsEnabled": false },
  "telemetry": { "enabled": false, "logPrompts": false }
}
```

- `usageStatisticsEnabled` is on by default and needs a restart to take effect.
- The `telemetry` block only exports to the user's own collector. It isn't a Google channel; setting it is hygiene.
- `/privacy` shows the privacy notice for the current auth type.
- Training follows the auth type:
  - API key: see section 4.
  - Vertex: Cloud terms apply, no training.

---

## 3. Antigravity (IDE, app, CLI): the consumer successor [V]

The terms say Google uses "Interactions" to improve its ML, that human reviewers may see them, and that you can opt out in settings. In other words, training is ON by default.

- **App / IDE**: Settings → `Account` → `Enable Telemetry` → OFF. The setting is described as "enable or disable sharing interaction logs to improve models".
  - The IDE has no separate toggle documented. It probably uses the same Account setting [U].
- **CLI**: run `/config` (alias `/settings`) → `Enable Telemetry` → OFF.
  - Optionally turn off `Show Feedback Survey` too.
  - On first run, **untick** the consumer telemetry checkbox.
  - Settings file: `~/.gemini/antigravity-cli/settings.json` (key `enableTelemetry`). The JSON shape is unverified, so change it through `/config` rather than editing the file.
- Business accounts (Cloud project / ADC) never collect prompts, so there's nothing to change.
- Deleting existing data has to be requested by email: antigravity-support@google.com. Confirm with the user before sending.

---

## 4. Gemini API / AI Studio

- **Free tier** [S]: prompts and responses are used to improve Google products, and humans may review them. **There is no toggle.**
  - The only fixes are moving the project to the paid tier (Cloud Billing enabled, which is a billing change, so confirm first) or not sending sensitive data.
  - In the EEA, UK and Switzerland, paid-tier data terms apply to every tier.
- **Paid tier**: Google doesn't use prompts or responses to improve products.
- **Logs** [V]:
  - Don't share logs or datasets with Google.
  - Untick sharing when creating a dataset.
  - **Don't join the "Contributor Tier"**. It means unpaid-tier data terms apply.

## 5. Jules [V partial]

The FAQ says Jules doesn't train on private repository content. No toggle is documented. Public repos aren't addressed, so report this to the user as "no setting; check jules.google.com/legal".
