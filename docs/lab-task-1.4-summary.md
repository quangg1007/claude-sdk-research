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


## Sample Output
### Scenario 1
User message: 
```
Handle a refund request for customer ID 123 for the amount of $750.
```

AI Agent:
```
I'll help you process this refund request. Let me start by checking the customer's information to verify eligibility.
Tool: mcp__server__get_customer
Excellent! Customer 123 (John Doe) is active and eligible for a refund. Now I'll process the refund of $750.
Tool: mcp__server__process_refund
The refund amount of $750 exceeds the $500 automatic refund limit. I'll escalate this request to a human agent for review and approval.
Tool: mcp__server__escalate_to_human
✅ **Refund Request Escalated**

The refund request has been successfully escalated to a human agent for review:

- **Customer ID:** 123
- **Customer Name:** John Doe
- **Refund Amount:** $750
- **Status:** Escalated to human-agent-queue
- **Reason:** Amount exceeds the $500 automatic refund limit

The customer's account is active and in good standing. A human agent will review this request and make a final determination on approval.
Done: success
```

### Scenario 2

User message: 
```
Handle a refund request for customer ID 123 for the amount of $150.
```

AI Agent:
```
I'll start by loading the necessary tool schemas, then check the customer's information first before proceeding with the refund.
Tool: ToolSearch
Great, the tools are loaded! Now let me check the customer's information first.

**Step 1: Look up Customer ID 123**
Tool: mcp__server__get_customer
Customer found! Here's what I know:
- **Name:** John Doe
- **Email:** john.doe@example.com
- **Status:** ✅ Active

The customer is **active and eligible** for a refund. Proceeding to process the refund now.

---

**Step 2: Process the $150 Refund**
Tool: mcp__server__process_refund
---

✅ **Refund Successfully Processed!**

Here's a summary of the completed transaction:

| Field | Details |
|---|---|
| **Customer** | John Doe (ID: 123) |
| **Email** | john.doe@example.com |
| **Refund Amount** | $150.00 |
| **Status** | ✅ Processed |

The refund of **$150** has been successfully issued to **John Doe**. No escalation was needed as the customer was active and all criteria were met.
Done: success
```