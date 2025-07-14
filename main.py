# main.py
#
# Streamlit app entry point for AI News Reporter.
# This app provides a web UI for users to ask about weather or news.
# The user's input is sent to a language model agent, which decides which tool to call (weather or news) on the my_info.py MCP server.
#
# Usage: streamlit run main.py

import streamlit as st
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up Streamlit UI
st.set_page_config(page_title="AI News Reporter", page_icon="📰")
st.title("📰 AI News Reporter")

st.markdown(
    """
    ### How does it work?
    This app uses an **MCP (Model Context Protocol) server** (`my_info.py`) to provide weather and news tools. When you ask a question, the AI agent communicates with the MCP server to fetch real-time information. MCP allows the agent to access modular tools in a standardized way, making the system flexible and extensible.
    """
)

st.sidebar.title("About")
st.sidebar.markdown(
    """
    **AI News Reporter**
    
    - Uses MCP (Model Context Protocol) servers to provide weather and news tools.
    - The AI agent decides which tool to use based on your question.
    - Powered by a language model agent.
    
    **What is MCP?**
    
    MCP is a protocol for exposing tools (functions, APIs, or services) to language model agents in a standardized way. In this project, the weather and news functionalities are provided as MCP tools via the `my_info.py` server.
    """
)

# Text input for user question
user_input = st.text_input("Ask me anything (weather or news):", "What's the weather in Bangalore?")

# Button to submit the question
submit = st.button("Ask")

# Async function to get agent response
async def get_agent_response(user_input):
    # Set up the MCP client to connect only to my_info server
    client = MultiServerMCPClient(
        {
            "my_info": {
                "url": "http://localhost:8000/mcp",  # my_info.py server must be running
                "transport": "streamable_http",
            }
        }
    )
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    tools = await client.get_tools()
    model = ChatGroq(model="qwen-qwq-32b")
    agent = create_react_agent(model, tools)
    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": user_input}]
    })
    return response['messages'][-1].content

# When the user submits a question
if submit and user_input.strip():
    with st.spinner("Thinking..."):
        # Run the async agent in Streamlit
        response = asyncio.run(get_agent_response(user_input))
        st.markdown(f"**Response:**\n{response}")

st.sidebar.info("Start the MCP server with: python my_info.py\n\nThen run this app with: streamlit run main.py")
