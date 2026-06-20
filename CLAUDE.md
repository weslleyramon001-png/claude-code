# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is the public **Claude Code** repository — home to official plugins, GitHub issue automation scripts, workflow definitions, and example configurations. The Claude Code CLI itself is closed-source; this repo is a companion resource for users and contributors.

## Scripts

Scripts live in `scripts/` and run with **Bun** (not Node):

```bash
# Dry-run the issue sweep (marks stale, closes expired)
bun run scripts/sweep.ts --dry-run

# Post a lifecycle nudge comment for a label
GITHUB_TOKEN=... GITHUB_REPOSITORY=owner/repo LABEL=stale ISSUE_NUMBER=123 bun run scripts/lifecycle-comment.ts --dry-run

# Auto-close confirmed duplicates
bun run scripts/auto-close-duplicates.ts --dry-run

# Backfill duplicate comments
bun run scripts/backfill-duplicate-comments.ts --dry-run
```

All scripts require `GITHUB_TOKEN`. Owner/repo are provided via `GITHUB_REPOSITORY_OWNER` + `GITHUB_REPOSITORY_NAME` (sweep) or `GITHUB_REPOSITORY` (others).

## GitHub Automation Architecture

Three layers of automation run on issues:

1. **Triage** (`claude-issue-triage.yml`) — fires on every new issue and non-bot comment. Runs `/triage-issue` via `claude-code-action`, which calls `scripts/edit-issue-labels.sh` to apply/remove labels. No comments are ever posted — label changes only.

2. **Deduplication** (`claude-dedupe-issues.yml`) — fires on new issues. Runs `/dedupe` via `claude-code-action`, which calls `scripts/comment-on-duplicates.sh` to post potential-duplicate links.

3. **Lifecycle sweep** (`sweep.yml`) — runs twice daily via cron. Executes `scripts/sweep.ts` directly with Bun to mark issues stale and close expired ones per the timeouts in `scripts/issue-lifecycle.ts`.

`scripts/issue-lifecycle.ts` is the single source of truth for lifecycle labels (`invalid`, `needs-repro`, `needs-info`, `stale`, `autoclose`), their timeouts in days, and their close reasons/nudge messages.

`scripts/gh.sh` is a locked-down `gh` CLI wrapper used inside Claude-driven workflows. It only permits `issue view`, `issue list`, `search issues`, and `label list` with a restricted flag set — no writes.

Authentication in all workflows uses **Workload Identity Federation** (OIDC token exchange) rather than a static API key, via `anthropic_federation_rule_id` / `anthropic_organization_id` / `anthropic_service_account_id` / `anthropic_workspace_id` workflow variables.

## Slash Commands (`.claude/commands/`)

| Command | Description |
|---|---|
| `/triage-issue` | Reads an issue and applies/removes labels using `gh.sh` and `edit-issue-labels.sh`. Never posts comments. |
| `/dedupe` | Finds up to 3 likely duplicate issues using parallel agents and posts them via `comment-on-duplicates.sh`. |

## Plugins Architecture

All plugins live under `plugins/` and follow this structure:

```
plugin-name/
├── .claude-plugin/plugin.json   # metadata (name, version, author, description)
├── commands/                    # slash commands (.md files with YAML frontmatter)
├── agents/                      # specialized sub-agents (.md files)
├── skills/                      # Skills (auto-invoked capabilities, each with SKILL.md)
├── hooks/                       # event handlers
└── .mcp.json                    # MCP server config (optional)
```

The marketplace manifest at `.claude-plugin/marketplace.json` lists all bundled plugins with their source paths. Commands use YAML frontmatter (e.g., `allowed-tools:`, `description:`) to declare permissions and metadata.

## Dev Container

`.devcontainer/` provides a sandboxed Claude Code development environment. The container runs as the `node` user, mounts the workspace at `/workspace`, and applies network restrictions via `init-firewall.sh` on startup. Claude config is persisted in a named volume at `/home/node/.claude`.
