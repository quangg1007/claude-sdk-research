from claude_agent_sdk import create_sdk_mcp_server, tool

server = create_sdk_mcp_server("refund-agent")

@tool(server)
def get_customer(customer_id: str) -> dict:
    """
    Get customer information by customer ID.
    """
    # Simulate fetching customer data from a database
    customers = {
        "123": {"name": "John Doe", "email": "john.doe@example.com", "status": "active"},
        "456": {"name": "Jane Smith", "email": "jane.smith@example.com", "status": "inactive"}
    }
    return customers.get(customer_id, {"error": "Customer not found"})

@tool(server)
def process_refund(customer_id: str, amount: float) -> dict:
    """
    Process a refund for a customer.
    """
    # Simulate refund processing logic
    if customer_id == "123":
        return {"status": "success", "message": f"Refund of ${amount} processed for customer {customer_id}"}
    else:
        return {"status": "error", "message": "Customer not found"}


@tool(server)
def escalate_to_human(customer_id: str, amount: float, reason: str) -> dict:
    """
    Escalate the refund request to a human agent for further review.
    """
    # Simulate escalation logic
    return {
        "status": "escalated", 
        "customer_id": customer_id,
        "amount": amount,
        "reason": f"Refund request for customer {customer_id}  has been escalated for review. Reason: {reason}",
        "assigned_to": "human-agent-queue"       
    }