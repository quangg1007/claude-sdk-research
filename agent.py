# import asyncio
# from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

# async def main():
#     # Agentic loop: streams messages as Claude works
#     async for message in query(
#         prompt="Review utils.py for bugs that would cause crashes. Fix any issues you find.",
#         options=ClaudeAgentOptions(
#             allowed_tools=["Read", "Edit", "Glob"],
#             permission_mode="acceptEdits"
#         )
#     ):

#         if isinstance(message, AssistantMessage):
#             for block in message.content:
#                     if hasattr(block, "text"):
#                         print(block.text)
#                     elif hasattr(block, "name"):
#                         print(f"Tool call: {block.name} with args {block.args}")
#         elif isinstance(message, ResultMessage):
#             print(f"Final result: {message.result}")

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def main():
    # Agentic loop: streams messages as Claude works
    async for message in query(
        prompt="Add docstrings to all functions in utils.py",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],  # Tools Claude can use
            permission_mode="acceptEdits",  # Auto-approve file edits
            model="claude-haiku-4-5"  # Specify the model to use
        ),
    ):
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)  # Claude's reasoning
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")  # Tool being called
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")  # Final result


asyncio.run(main())