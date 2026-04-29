# Lab Task 1.4 — Refund Agent with Hooks & Human Escalation

## Scenario

A refund agent that must verify a customer before processing a refund. If the refund exceeds $500, it escalates to a human agent instead of processing automatically.

## Tools (MCP)

| Tool | Inputs | Returns |
|---|---|---|
| `get_customer` | `customer_id: str` | Mock customer data (name, account status) |
| `process_refund` | `customer_id: str`, `amount: float` | Mock success confirmation |
| `escalate_to_human` | `customer_id: str`, `amount: float`, `reason: str` | Structured handoff summary |

## Hook requirements

### 1. Prerequisite gate (`PreToolUse`)
- Fires before every tool call
- If the tool is `process_refund` and `get_customer` has **not** been called yet in this session → block the call and tell the agent it must call `get_customer` first

### 2. Policy enforcement (`PreToolUse`)
- Fires before every tool call
- If the tool is `process_refund` and `amount > 500` → block the call and tell the agent to use `escalate_to_human` instead

## Human handoff

When `escalate_to_human` is called, it returns a structured dict as the tool result:

```python
{
    "status": "escalated",
    "customer_id": "...",
    "amount": ...,
    "reason": "...",
    "assigned_to": "human-agent-queue"
}
```

The agent should surface this as its final response message.

## Implementation steps

1. MCP server with the 3 tools
2. `agent.py` wiring up the MCP server and sending a refund prompt
3. `PreToolUse` hook — prerequisite gate
4. `PreToolUse` hook — policy enforcement
5. Test: happy path (≤ $500, customer verified) and escalation path (> $500)

## Files

```
agent.py              # Entry point — query() loop
mcp_server.py         # MCP tool definitions
```
