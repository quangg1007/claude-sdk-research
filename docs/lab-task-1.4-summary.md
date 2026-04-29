# Lab Task 1.4 — Summary & Post-Mortem

## What we built

A refund agent using `claude_agent_sdk` where Claude is the agent and tools are in-process MCP tools.

**Files:**
- `mcp_server.py` — 3 MCP tools: `get_customer`, `process_refund`, `escalate_to_human`
- `agent.py` — agentic loop with 2 `PreToolUse` hooks

**Two hooks:**
- `prerequisite_gate` — blocks `process_refund` if `get_customer` hasn't been called yet
- `exceed_limit` — blocks `process_refund` if `amount > 500`, forcing escalation

---

## Bugs hit & lessons learned

| # | Bug | Root cause | Fix |
|---|---|---|---|
| 1 | `AttributeError: 'str' has no attribute 'name'` | `tools=["get_customer", ...]` — strings instead of function objects | `tools=[get_customer, ...]` |
| 2 | `unhashable type: 'dict'` | Tool functions used individual params; SDK passes a single `args` dict | `async def get_customer(args): customer_id = args["customer_id"]` |
| 3 | `missing 2 required positional arguments` | Same as #2 | Same fix |
| 4 | Tools returned raw dicts | MCP protocol requires a content envelope | `return {"content": [{"type": "text", "text": json.dumps(result)}]}` |
| 5 | `exceed_limit` hook never fired | Hook matcher used short names (`process_refund`) but actual tool names are prefixed (`mcp__server__process_refund`) | Update matchers and comparisons to full names |
| 6 | `hooks` format wrong | Passed a list `[HookMatcher(...)]`; SDK expects `dict[HookEvent, list[HookMatcher]]` | `hooks={"PreToolUse": [HookMatcher(...)]}` |

---

## Key SDK facts to remember

- `@tool(name, description, input_schema)` — not `@tool(server)`
- `input_schema` values are Python types: `str`, `float` — not `"string"`, `"number"`
- MCP tool names follow the pattern: `mcp__{server_key}__{tool_name}`
- Hook `input["tool_name"]` uses the full prefixed name
- `called_tools` (the set tracking state) must also store full prefixed names
