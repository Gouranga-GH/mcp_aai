# AI News Reporter

AI News Reporter is a conversational Python application that uses AI, real-time APIs, and the Model Context Protocol (MCP) to provide:
- **Current weather information** for any location (using Open-Meteo, no API key required)
- **Latest news headlines** for any topic (using SerpAPI, requires a free API key)

The app uses a language model agent to decide which tool to call based on your natural language input. Just ask a question, and the AI will fetch the information for you!

---

## What is MCP (Model Context Protocol)?

**MCP** is a protocol for exposing tools (functions, APIs, or services) to language model agents in a standardized way. In this project, the weather and news functionalities are provided as MCP tools via the `my_info.py` server. The Streamlit UI (`main.py`) communicates with the MCP server, allowing the AI agent to dynamically decide which tool to use based on your question.

---

## Features
- **Conversational interface:** Just type your question, no menus or commands needed.
- **Weather tool:** Real-time weather for any city or place, powered by Open-Meteo and OpenStreetMap, exposed as an MCP tool.
- **News tool:** Top news headlines for any topic, powered by SerpAPI (Google News), exposed as an MCP tool.
- **Beginner-friendly:** Well-commented code and easy setup.
- **Modern architecture:** Uses MCP servers for modular, scalable tool integration.

---

## Project Structure

```
AI News Reporter/
├── client.py      # (Optional) CLI interface for development/testing
├── my_info.py     # MCP server providing weather and news tools
├── main.py        # Streamlit UI (entry point)
├── pyproject.toml # Project dependencies
├── requirements.txt # (optional) Additional dependencies
├── .env           # Your API keys (not included by default)
├── README.md      # This file
```

---

## Setup & Usage

1. **Install dependencies using [uv](https://github.com/astral-sh/uv) (recommended):**
   ```sh
   uv pip install -r pyproject.toml
   ```
   Or use pip:
   ```sh
   pip install -r requirements.txt
   ```

2. **Set up your `.env` file:**
   - Create a file named `.env` in the project root.
   - Add your SerpAPI key (get one for free at https://serpapi.com/):
     ```
     SERPAPI_KEY=your-serpapi-key-here
     ```
   - (No API key is needed for weather.)

3. **Start the MCP server:**
   ```sh
   python my_info.py
   ```

4. **In a new terminal, run the Streamlit UI:**
   ```sh
   streamlit run main.py
   ```

5. **Ask your questions in the web interface!**
   - Example: `What's the weather in London?`
   - Example: `Show me news about AI.`

---

## Environment Variables
- `SERPAPI_KEY` — Required for news tool. Get it from [serpapi.com](https://serpapi.com/).
- No key is needed for weather.

---

## Credits
- [Open-Meteo](https://open-meteo.com/) for free weather data
- [Nominatim (OpenStreetMap)](https://nominatim.org/) for geocoding
- [SerpAPI](https://serpapi.com/) for news headlines
- [LangChain](https://python.langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/) for agent and tool orchestration
- **Model Context Protocol (MCP)** for modular tool integration

---

## License
This project is for educational and personal use. See LICENSE for details.
