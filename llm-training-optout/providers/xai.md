# xAI: Grok (grok.com, apps), Grok on X, xAI API, Grok Build

Verified 2026-10-20. x.ai and help.x.com block automated fetching, so most items come from Wayback snapshots of the official pages, taken 2026-10-02 and 2026-10-12 [V-arc]. docs.x.ai was fetched live [V]. [U] marks items I couldn't verify. xAI pages may now be branded "SpaceXSI".

---

## 1. Grok (grok.com, iOS, Android)

**Sign in first.** In some regions outside the EU/UK, logged-out users can't opt out of training [V-arc].

### Required: turn off "Improve the Model" [V-arc] (x.ai/legal/faq)
- Mobile: `Settings` → `Data Controls` → `Improve the model` → OFF.
- grok.com: Profile → `Settings` → `Data` or `Data Controls` (the label varies) → `Improve the Model` → OFF.
- Default is ON. Only new conversations are affected, not past ones.
- It also covers voice input, because audio counts as User Content, and Build-mode sessions on grok.com and mobile.

### Never do while working
- Don't give thumbs or other feedback. Feedback "may be used for training" even after opt-out [V-arc].

### Optional (ask first)
- `Personalize Grok using X`: personalization only, not training. Same Data Controls screen.
- Memory: possibly labelled "Personalize Grok with your conversation history" [U, from a third-party source].
- Private Chat (ghost icon, top right): not used for training, deleted within 30 days. Mention it as an option. It isn't available in Build mode.
- Deletion is destructive, so confirm first. Path: Data Controls → `Delete All Conversations`. Shared links: grok.com/share-links.

---

## 2. Grok on X (x.com, X apps)

### Required [V-arc, exact label] (help.x.com/en/using-x/about-grok)
- Path: X `Settings and privacy` → `Privacy & Safety` → `Data sharing and personalization` → `Grok & Third-party Collaborators`.
- Deep link: https://x.com/settings/grok_settings [S].
- Under "Data Sharing", **untick**: "Allow your public data as well as your interactions, inputs, and results with Grok and xAI to be used for training and fine-tuning."
- The same screen has "Allow X to personalize your experience with Grok". It's optional; ask first.
- The setting may be web-only or behave differently in the EU [U]. If the mobile app doesn't show it, use x.com in a browser.
- Limits: deployed Grok features on X can still learn "through normal use", and feedback may still be used.

### Optional (ask first)
- Delete Grok-on-X history (destructive): `Privacy & Safety` → `Data sharing and personalization` → `Grok` → `Delete Conversation History`.
- `Protect your posts` (under `Audience and tagging`) keeps posts out of training, but it makes the account private. That's a major change, so only do it on an explicit request.

---

## 3. xAI API (console.x.ai) [V] (docs.x.ai security FAQ)
- No training on API data "without your explicit permission". Requests and responses are kept 30 days for abuse auditing.
- Check Console → Billing / Team settings for any **data-sharing-for-credits** opt-in, and make sure it isn't enabled. The current label is unverified [U].
- Optional: Zero Data Retention is under `Team Settings` → `Zero Data Retention (ZDR)` → `Enable`. Only a team admin can turn it on. It disables Files, Batch and stateful Responses, so confirm first.

## 4. Grok Build (xAI coding CLI) [V] (docs.x.ai/build)
- Run `/privacy` to see or toggle data retention, or go through `/settings`. Turn off code-data retention / "improve the product and model".
- On first run, decline the screen that asks to retain data to improve the product and model.
- Config lives in `config.toml` and history in `~/.grok/`. The exact keys are unverified [U], so use the slash commands rather than editing files.
