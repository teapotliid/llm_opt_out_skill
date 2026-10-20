# Meta: Muse Spark, Meta AI (app, meta.ai, WhatsApp, Instagram, Facebook, Messenger), Muse agent, Vibes

Verified 2026-10-20. Tags:
- [V] official Meta page fetched
- [V-mirror] official text via a verbatim third-party mirror
- [3P] third-party source
- [S] search result only
- [U] unverified

Meta renames settings often, and many Meta help pages render client-side. If a label below isn't on screen, search Settings for "Data", "privacy", "AI", "Manage your information". Don't flip anything you can't identify.

> **Muse Spark** (announced 2026-04-08) is a Meta Superintelligence Labs **model**, not an app. It powers Meta AI in the Meta AI app and on meta.ai, and press reports say it also powers WhatsApp and Instagram. It also powers the separate **Muse** agent app [V]. Muse Spark has no settings of its own. Data rules depend on which surface the user reaches it through:
>
> | Surface | Training control |
> |---|---|
> | Meta AI app / meta.ai / Meta AI in WhatsApp, IG, FB, Messenger | **No opt-out** in the US and most regions. EU/UK and some other countries have an objection form (§4) |
> | Muse agent app (muse.ai, "Muse from Meta") | **Has a toggle**, and it is retroactive (§2) |
> | Meta Model API (dev.meta.ai) | Set by which model ID you call (§6) |

---

## 1. Meta AI app (iOS/Android, formerly Meta View) and meta.ai

### Training: no toggle exists [V]

Every Meta AI help page says "Meta uses your interactions with AIs to improve AI at Meta." The AI Terms (effective 2026-05-13) [V-mirror] add that conversations may be reviewed by humans and shared with select partners such as search engines. They also say deleting messages or the account "may not delete our copy".

**Don't search for a training switch.** Report "no opt-out available (region: ___)". Then:
- Do the cleanup steps below (ask first).
- Tell the user about Incognito chat.
- Use the objection form if the user is in a covered region (§4).

### Never do while working
- Don't tap **Share / Post** on any chat or image. Posting publishes it to the public Vibes/Discover feed. Profiles are public across the Meta AI app, the Vibes app, meta.ai and vibes.ai [V].
- Don't give feedback on responses.

### Cleanup (destructive: confirm first) [V] (help pages 2457110494637611, 1771195753735844)
Path in the app: Menu (top left) → `Settings` (bottom left) → under App settings, `Data & privacy` → `Manage your information`. On that screen:
- `Delete all chats and media` → `Delete all`. This removes chats, prompts and media from History. It doesn't delete public vibes.
- `Remove all public vibes` → `Remove all`. This takes your posts off the public feed.
- `Export your information` / `Download your information`. Offer this before deleting.

Web and desktop labels are unverified [U]. On meta.ai, look under Settings for the same items.

Older press mentions a toggle labelled "Make all your prompts visible to only you". It's absent from the current official page [V], so if it's still there, turn it ON.

### Other controls
- **Incognito chat** (announced 2026-05-13 for WhatsApp and the Meta AI app, rolling out): WhatsApp says it's built on Private Processing, "not saved", and that "no one can read your conversation, not even us" [V]. No official page explicitly says these chats aren't used for training [U]. Recommend it to the user for sensitive questions, but don't claim it guarantees no training.
- **Memory** (US/Canada): there's no documented Settings toggle [U]. To view memory, ask Meta AI "what do you remember about me?". To remove items, ask it to forget them one at a time. Deleting a chat also deletes the memories drawn from it [V].
- **Ads:** since 2025-12-16, AI chats are used to personalize content and ads in most regions, with **no opt-out** [V, about.fb.com 2025-10-01]. WSJ reports this excludes the UK, EU and South Korea [S].
  - Sensitive topics are excluded, per Meta.
  - The one lever: Meta AI chats in WhatsApp only feed cross-app ads if WhatsApp is in the **same Accounts Center** as Facebook and Instagram. Tell the user; don't change Accounts Center without asking.
- **Vibes** (AI video feed): there's no Vibes-specific training control. To remove one vibe: Menu → profile → the vibe → Menu → `Remove from feed`.

---

## 2. Muse agent app (muse.ai; iOS/Android "Muse from Meta"; US launch 2026-09-08)

### Required [V] (help 2225571704857152; Muse Privacy Policy, effective 2026-09-17)
- Path: `Settings` → `Data controls` → **`Help improve our AI models`** → OFF → confirm `Turn off`.
- Default is ON ("This setting is on when you first use Muse").
- The change **also applies to previous interactions**, and it covers Connector data too.

### Optional (ask first)
- `Settings` → `Data controls` → `Download your Muse data`.
- `Settings` → `Data controls` → `Reset Muse` deletes everything and can't be undone. Muse may still remember information it learned from what you deleted.
- Memory: Assistant icon → `Identity` → `Memory`. This opens an editable MEMORY.md.

### Account separation [V]
Muse doesn't share conversations or VM data with Meta's ad systems. If the Muse account is kept separate (signed up with an email not tied to an existing Meta account), Muse data isn't shared with other Meta products. Recommend this to new users.

---

## 3. Meta AI inside WhatsApp, Instagram, Facebook, Messenger

You can't turn Meta AI off in any of these apps [3P]. There's also no training toggle.

### WhatsApp
- **Delete Meta AI's copy of a chat (destructive: confirm first):**
  1. In the Meta AI chat, send `/reset-ai`. Use `/reset-all-ais` to cover all chats [3P, citing faq.whatsapp.com/688464770796037].
  2. Then long-press the chat → `Delete chat`.
- **Restricted chat** (formerly "Advanced Chat Privacy") blocks Meta AI in a chat, along with export and auto-download.
  - Android: chat → View contact → `Restricted chat` → ON.
  - iPhone: chat → name → `Restricted chat`.
  - Only admins can set it in a group. An older ACP chat needs `Upgrade`. Labels are [3P], and rollout is mixed.
  - This one is optional: it changes the chat for the other people in it too, so ask first.
- **Private Processing:** `Settings` → `Chats` → `Private Processing`. It's off by default and powers AI summaries. Leave it off unless the user wants those features.
- **Accounts Center:** keeping WhatsApp out of the Facebook/Instagram Accounts Center stops WhatsApp Meta AI chats feeding cross-app ads [V].

### Instagram, Facebook, Messenger
- To delete AI messages, type `/reset-ai` in the Meta AI conversation [3P, quoting Meta]. Confirm first.
- Accounts Center has no AI-training toggle [V].

---

## 4. Objection forms (EU/UK and some other countries) [V] (help 4532990443643263)

These let the user object to their **AI interactions and public content** being used to train AI at Meta. One submission covers the logged-in account plus every account in the same Accounts Center.

| Platform | Form |
|---|---|
| Facebook | https://www.facebook.com/help/contact/6359191084165019 |
| Instagram | https://help.instagram.com/contact/233964459562201 |
| WhatsApp | https://www.facebook.com/help/contact/481841188140300 ("only available to people in certain regions") |
| Meta account (Muse / Meta AI) | linked from the help page above (auth.meta.com form) |

- **Submitting is outward-facing.** Fill in the form, show it to the user, and submit only after they say yes.
- In the US there's no equivalent. If the form says it's unavailable in the user's region, report that.
- **Personal info appearing in AI answers** (users and non-users):
  - AU, BR, EC, EU, ID, NG, PH, RS, ZA, KR, TH, TR, UK: https://www.facebook.com/help/contact/510058597920541
  - All other countries: https://www.facebook.com/help/contact/1266025207620918
- **Public posts:** EU training on public posts and comments began 2025-05-27 [S]. Making an account private (or limiting past posts) keeps *future* posts out of the public-content pool. Whether content that was already trained on gets removed is not stated [U]. This is a big change to the account, so only do it on explicit request.
- Meta says it doesn't train on private messages with friends and family, unless someone in the chat shares them with Meta AI [V, about.fb.com note dated 2026-03-27].

---

## 5. AI glasses (Ray-Ban Meta Gen 1–3, Ray-Ban Meta Audio, Oakley Meta, Meta Ray-Ban Display, Meta Glasses line) and Quest

All glasses settings are in the **Meta AI mobile app** (formerly Meta View). Help articles use this common path [V]:
`Glasses` (top right) → `Device settings` → *your glasses* (with several pairs, swipe to pick one) → `Glasses privacy`.

Labels shift between app versions. Match on "privacy", "Voice activity", "Experiences" and "Meta AI". **The glasses must be out of the case and connected to the phone. Repeat for each pair.**

### Required

1. **Visual data** [V] (help 1381548946634724, Sept 2026)
   - Path: glasses Settings → `Experiences` → `Meta AI` → **`Store visual data from AI experiences`** → OFF.
   - Default is ON. Live AI and "look and ask" images are stored, used for training, and may be reviewed by humans.
   - With it OFF, those images are not stored after processing, not used for training, and not reviewed by humans.
   - It isn't retroactive. It doesn't cover voice, images sent to Meta AI in Messenger or Instagram, or metadata such as AI-generated image descriptions.
   - Ray-Ban Meta Audio has no camera, so skip this step for it.
2. **Cloud media** [V]: `Glasses privacy` → `Cloud media` → OFF. Media processed in the cloud is otherwise held for 30 days. Turning it off may break voice-initiated photo sharing, so tell the user.
3. **Additional Data (usage analytics)** [V]: `Glasses privacy` → the additional-data toggle → OFF. The label isn't captured; older builds said "Share additional data" [U]. The choice applies to all paired glasses and wrist devices.
4. **Voice recordings.** These depend on region [V]:

   | Region | Behavior | Action |
   |---|---|---|
   | US, Canada, Australia, Singapore | Stored by default, kept up to 1 year, may be reviewed by humans. **No storage opt-out:** "The option to disable voice recordings storage is no longer available." | Report "no opt-out". Offer the optional controls below. |
   | UK, Ireland, Germany / EU, Brazil | Storage is opt-in. When it's off, recordings are deleted right after processing. | `Glasses privacy` → voice storage toggle (EU label reportedly "Save Voice Interactions") → OFF. This isn't retroactive. |
   | South Korea, India | Audio storage is opt-in. Transcripts are stored by default and can be changed in Settings. | Turn both off. |

### Optional (ask first)

- **Delete voice history** (destructive): `Glasses privacy` → `Voice activity log` → delete entries, or use delete-all. The exact button label is unverified [U].
- **Reduce voice capture:** `Meta AI` → `"Hey Meta" preferences` → `Respond without "Hey Meta"` → OFF. This is ON by default.
  - The user could also turn off the "Hey Meta" wake word entirely. That disables voice and camera AI features, so it's a big change and needs an explicit request.
- **Delete live-AI transcripts and camera queries:** in the Meta AI app, Menu (top left) → `Chats`.
- **Meta Neural Band:** wrist sensor data reaches Meta only when the user submits a bug report. Avoid bug-report flows. Deletion requests go to https://help.meta.com/support/privacy.
- **Quest:** transcripts are stored by default and voice recordings are opt-in. To view or delete: headset → Quick settings → `Settings` → `Meta AI` → `Activity log`.

---

## 6. Developer products

### Meta Model API (llama.developer.meta.com = dev.meta.ai; replaced the Llama API) [V] (ToS 2026-10-09)

- **Standard model IDs are never trained on** (ToS §5.1). **`-contributor` model IDs are trained on** (§6.1). Contributor IDs include `muse-spark-1.3-contributor` and `muse-spark-1.2-contributor`.
  - **Check the user's code and config for model IDs ending in `-contributor`.** Report any you find. Don't edit their code unasked.
  - Submitting content that was previously sent to a Standard model in a Contributor request makes that content Contributor data.
  - The ToS warns that the system "may route you to a Contributor Model".
- **Usage Data** (tool-call sequences, logs, telemetry) may be used to improve the service. There's no opt-out.
- **No console data toggle exists** for pay-as-you-go.
- **Zero Data Retention** is org-level and only available through sales. Mention it to the user; it isn't an action the agent can take.

### Muse Code (`muse` CLI) [V]

- **Subscriptions default to Contributor mode.** Prompts, code, files, context and responses are used to train.
  1. Check `muse --version` is **at least 1.4.8**. Earlier builds still sent background requests after opt-out. Updating is a software change, so ask first.
  2. In `muse`, run **`/settings`** → **Contributor mode** → OFF. The toggle only appears with an active subscription. The change applies going forward only.
- **API-key users** (`META_API_KEY` or `muse auth set`): training follows the model ID. The default model, `muse-spark-1.2`, is Standard. Don't select `-contributor` models.
- **Telemetry** (handled by `scripts/optout_cli.py`, via the env file):
  - `TBH_DISABLE_TELEMETRY=1` and `TBH_DISABLE_FEATURE_CONFIG=1`.
  - These are **undocumented internal variables** found in Meta's official SDK test harness (github.com/meta-models/muse-code-sdk) [V-source], so they may change. Tell the user.
  - `~/.config/muse/settings.json` contains "telemetry options", but the key names aren't published [U]. Inspect the file and report what the installed build shows. **Don't invent keys.**
- **Local history (optional):**
  - `MUSE_SKIP_PROMPT_HISTORY=1` stops new prompts being saved to local history.
  - `--no-session-log` stops the local session log.
  - `session_retention_days` sets how long local sessions are kept.
- **Don't use `/feedback`.** It uploads session records and traces.

### Others

- **Self-hosted weights** (Llama 3.x/4, Muse Spark Open, Muse Glimmer): nothing is sent to Meta.
- **Llama Stack, now "OGX"** (ogx-ai/ogx): OpenTelemetry is sent only to the user's own `OTEL_EXPORTER_OTLP_ENDPOINT`. There's nothing to opt out of.
- **Meta AI Studio** (custom AIs): covered by the AIs Terms, which say chats are used to "improve AI at Meta". There's no product-specific toggle. Use the §4 objection forms where available.
- **Meta Business Agent** (WhatsApp Business): "Paused for new chats but learning" keeps collecting chats. If the user wants no learning, remove or don't set up the agent; ask first. Whether these chats train Meta's general models is unconfirmed [U].
