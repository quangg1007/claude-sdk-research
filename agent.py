import asyncio
from claude_agent_sdk import ClaudeAgentOptions, query, AssistantMessage, ResultMessage, HookMatcher
from mcp_server import server, get_customer, process_refund, escalate_to_human

# `set` is like a bag that remembers which tool names have been called.
# It ignores duplicates, so adding "get_customer" twice still counts as one.
called_tools = set()


system_prompt = """
You are a customer service agent responsible for handling refund requests.
When a refund request is received, you should first check the customer's information using the `get_customer` tool.
If the customer is active and eligible for a refund, you can process the refund using the `process_refund` tool.
If the customer is inactive or if there are any issues with the refund request, you should escalate the request to a human agent using the `escalate_to_human` tool, providing the reason for escalation.

Process a refund of $150 for customer ID 123.
"""


async def prerequisite_gate(input, tool_use_id, context):
    tool_name = input["tool_name"]

    # If process_refund is about to run but get_customer hasn't been called yet — block it.
    if tool_name == "process_refund" and "get_customer" not in called_tools:
        return {
            "decision": "block",
            "reason": "You must call get_customer first to verify the customer before processing a refund.",
        }

    # Otherwise, record that this tool ran and allow it.
    called_tools.add(tool_name)
    return {}


async def exceed_limit(input, tool_use_id, context):
    tool_name = input["tool_name"]
    if tool_name == "process_refund":
        amount = input["tool_input"]["amount"]
        if amount > 500:
            return {
                "decision": "block",
                "reason": "Refund amount exceeds the $500 limit. Please escalate to a human agent.",
            }
    return {}


options = ClaudeAgentOptions(
    mcp_servers={"server": server},
    allowed_tools=["mcp__server__get_customer", "mcp__server__process_refund", "mcp__server__escalate_to_human"],
    system_prompt=system_prompt,
    hooks={
        "PreToolUse": [
            HookMatcher(
                matcher="get_customer|process_refund|escalate_to_human",
                hooks=[prerequisite_gate],
            ),
            HookMatcher(
                matcher="process_refund",
                hooks=[exceed_limit],
            )
        ]
    }
)

prompt="Handle a refund request for customer ID 123 for the amount of $750."

async def main():
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")


asyncio.run(main())
