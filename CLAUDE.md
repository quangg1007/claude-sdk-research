# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Hands-on lab project for the **Claude Certified Architect – Foundations** exam. The goal is to explore and experiment with the `claude-agent-sdk` Python package — specifically the agentic loop pattern where a Python script drives Claude Code to autonomously read and modify files.

## Collaboration guidelines

- **Each branch is one lab.** Branch name maps to the lab task (e.g. `feat/lab-task-1.4`).
- **Requirement docs live in `docs/`.** Only write or update docs when explicitly permitted by the user.
- **Tutor mode.** Guide the user to implement tasks themselves — do not write code directly unless asked. Break work into steps, explain the concept behind each step, and ask before moving to the next.
- **Ask before assuming.** If a requirement is ambiguous, ask a clarifying question rather than making a design decision silently.

## Setup

```bash
# Activate the virtual environment
source .venv/bin/activate

# API key is loaded from .env (ANTHROPIC_API_KEY=...)
```

No install step is needed — dependencies are already in `.venv/`.

## Running

```bash
# Run the agent script
python agent.py
```

## Project Structure

```
agent.py           # Main entry point — drives the agentic loop
my-agent/utils.py  # Target file for Claude to operate on (read/edit)
.env               # ANTHROPIC_API_KEY
.venv/             # Python 3.10 virtualenv with claude-agent-sdk==0.1.71
```

## SDK Architecture

The `claude_agent_sdk` package works by spawning the Claude Code CLI as a subprocess (bundled at `_bundled/claude`) and communicating via a JSON control protocol over stdin/stdout.

### Key API surface

**`query(prompt, options)`** — async generator for one-shot interactions. Use this for fire-and-forget tasks. Yields message objects as Claude works.

**`ClaudeSDKClient`** — bidirectional client for interactive/stateful sessions. Supports `connect()`, `interrupt()`, `set_permission_mode()`, and `async with` usage.

**`ClaudeAgentOptions`** — configuration for a query/session:
- `allowed_tools` / `disallowed_tools` — e.g. `["Read", "Edit", "Glob"]`
- `permission_mode` — `"acceptEdits"` auto-approves file edits; `"bypassPermissions"` skips all prompts
- `model` — e.g. `"claude-haiku-4-5"`, `"claude-sonnet-4-6"`
- `max_turns`, `max_budget_usd`, `cwd`, `mcp_servers`, `hooks`

### Message types to handle in the loop

| Type | When it fires |
|---|---|
| `AssistantMessage` | Claude text output or tool use (`TextBlock`, `ToolUseBlock`) |
| `ResultMessage` | Terminal message — `subtype` is `"success"` or `"error"` |
| `RateLimitEvent` | Rate-limit hit; includes `retry_after_ms` |

### MCP server support

Use `create_sdk_mcp_server()` and the `@tool()` decorator to define in-process MCP tool servers and pass them to `ClaudeAgentOptions(mcp_servers=[...])`.

### Session management helpers

`list_sessions()`, `fork_session()`, `get_session_messages()`, `delete_session()` — available for stateful multi-turn lab exercises.
