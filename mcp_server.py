import json
from claude_agent_sdk import create_sdk_mcp_server, tool


@tool(name="get_customer", description="Get customer information by customer ID.", input_schema={"customer_id": str})
async def get_customer(args):
    customer_id = args["customer_id"]
    customers = {
        "123": {"name": "John Doe", "email": "john.doe@example.com", "status": "active"},
        "456": {"name": "Jane Smith", "email": "jane.smith@example.com", "status": "inactive"},
    }
    result = customers.get(customer_id, {"error": "Customer not found"})
    return {"content": [{"type": "text", "text": json.dumps(result)}]}


@tool(name="process_refund", description="Process a refund for a customer.", input_schema={"customer_id": str, "amount": float})
async def process_refund(args):
    customer_id = args["customer_id"]
    amount = args["amount"]
    result = {
        "status": "refund_processed",
        "customer_id": customer_id,
        "amount": amount,
    }
    return {"content": [{"type": "text", "text": json.dumps(result)}]}


@tool(name="escalate_to_human", description="Escalate a refund request to a human agent.", input_schema={"customer_id": str, "amount": float, "reason": str})
async def escalate_to_human(args):
    customer_id = args["customer_id"]
    amount = args["amount"]
    reason = args["reason"]
    result = {
        "status": "escalated",
        "customer_id": customer_id,
        "amount": amount,
        "reason": reason,
        "assigned_to": "human-agent-queue",
    }
    return {"content": [{"type": "text", "text": json.dumps(result)}]}


server = create_sdk_mcp_server(
    name="refund-agent",
    tools=[get_customer, process_refund, escalate_to_human],
)
