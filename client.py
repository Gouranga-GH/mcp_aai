# client.py
#
# Part of the AI News Reporter project.
# This script provides a conversational interface for users to ask for weather or news.
# The user's input is sent to a language model agent, which decides which tool to call (weather or news) on the my_info.py server.
#
# Usage: Run this script, then type your question (e.g., "What's the weather in Paris?" or "Show me news about AI").
# Type 'exit' to quit.

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    # Set up the MCP client to connect only to my_info server (weather and news tools)
    client = MultiServerMCPClient(
        {
            "my_info": {
                "url": "http://localhost:8000/mcp",  # my_info.py server must be running
                "transport": "streamable_http",
            }
        }
    )

    # Ensure the GROQ_API_KEY is available for the language model
    import os
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Discover available tools and set up the language model agent
    tools = await client.get_tools()
    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model, tools)

    # Conversational loop: user types a question, agent decides which tool to call
    while True:
        user_input = input("\nAsk me anything (type 'exit' to quit): ")
        if user_input.strip().lower() == "exit":
            break
        response = await agent.ainvoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        print("Response:", response['messages'][-1].content)

if __name__ == '__main__':
    asyncio.run(main())
