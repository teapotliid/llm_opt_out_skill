# llm-training-optout skill

This is an agent skill that turns off model training and data sharing on your own AI accounts. It also hardens the local configs of your coding-agent CLIs.

## Install

Copy the folder into your agent's skills directory:

```bash
# Claude Code (user-level)
cp -r llm-training-optout ~/.claude/skills/
# Codex
cp -r llm-training-optout ~/.codex/skills/
```

Other harnesses that read `SKILL.md`-style skills (frontmatter `name` and `description`) work the same way. Harnesses without skill support can be given `SKILL.md` as instructions directly.

## Use

Ask your agent to "opt me out of AI training on ChatGPT, Claude and Doubao", or to "audit my AI privacy settings". To drive web and app settings pages, the agent needs computer use or browser control, and you need to be signed in already.

To run only the local part:

```bash
python3 llm-training-optout/scripts/optout_cli.py --dry-run
python3 llm-training-optout/scripts/optout_cli.py
cd llm-training-optout/scripts && python3 -m unittest test_optout_cli   # tests
```

## Layout

- `SKILL.md`: rules, workflow and a quick-reference table
- `providers/*.md`: per-vendor steps with verification tags
- `scripts/optout_cli.py`: patches Claude Code, Codex, Gemini CLI and Kimi Code configs, and writes one sourceable env file for CodeBuddy, DeepSeek Harness, Kimi and Meta Muse Code. Edits are backed up and idempotent.
- `templates/withdrawal_request_zh.md`: a PIPL / GB/T 45654 consent-withdrawal letter, for Chinese products that have no toggle

Raw research with sources is in `../optout_research/`.

## Maintenance

Settings labels move. Every provider file carries a "Verified YYYY-MM-DD" line and per-item tags ([V] official, [V-A]/[V-arc] official via archive, [3P] third party, [U] unverified). Re-verify the [U] items and anything older than about three months before relying on them.
