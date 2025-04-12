# JIRA MCP Chatbot

A conversational AI assistant built with DSPy and Streamlit that helps users query and interact with JIRA data through natural language.

## Project Overview

![MCP airbnb Assistant](https://raw.githubusercontent.com/ThanabordeeN/DSPy_MCP_Airbnb_Chat/main/image/app.png)

This project implements an AI-powered airbnb assistant that can answer questions, find tickets, and provide insights about airbnb data through natural language conversations. The system uses:

- **DSPy**: A framework for programmatically controlling language models
- **Streamlit**: For building the interactive web interface
- **FastAPI**: For the backend API server
- **MCP (Model Control Protocol)**: For managing the communication with various tool servers [DSPy Unofficial](https://github.com/ThanabordeeN/dspy-mcp-intregration.git)

## Architecture

The project consists of two main components:

### 1. Backend (FastAPI Server)
- Handles communication with DSPy and the language model
- Manages MCP server connections to JIRA through the Atlassian MCP server
- Implements the ReAct agent for reasoning and tool use
- Maintains conversation history

### 2. Frontend (Streamlit App)
- Provides a chat interface for users
- Sends queries to the backend
- Displays responses from the AI assistant

## Setup Instructions

### Prerequisites
- Python 3.9+
- API key for Google Gemini (or other compatible LLM)
- JIRA account with API access token

### Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd jira_mcp
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   export GOOGLE_API_KEY=your_api_key_here
   ```

### Configuration

The MCP server configuration is located in `backend/servers_config.json`. This file defines the JIRA connection details including URL, username, and token. You can use the `servers_config.example.json` file as a template.

## Running the Application
0. Install DSPy (MCP Version - Unofficial):
   ```bash
   git clone https://github.com/ThanabordeeN/dspy-mcp-intregration.git && cd dspy-mcp-intregration && pip install .
   ```

1. Start the backend server:
   ```
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8001 --reload
   ```

2. In a separate terminal, start the Streamlit frontend:
   ```
   streamlit run main.py
   ```

3. Open a web browser and navigate to `http://localhost:8501`

## Usage

1. Enter your JIRA-related questions in the chat input
2. The assistant will process your query, potentially using JIRA tools from the MCP server
3. Review the response in the chat interface

## Example Queries

- "Show me all critical bugs assigned to me"
- "What's the status of the authentication project?"
- "List open tickets in the frontend component"
- "Who's working on the most tickets this sprint?"

## Project Structure

```
jira_mcp/
├── README.md                          # This documentation
├── main.py                            # Streamlit frontend
├── .gitignore                         # Git ignore file
├── backend/
│   ├── main.py                        # FastAPI backend server
│   ├── servers_config.json            # MCP server configuration
│   └── servers_config.example.json    # Example config template
└── requirements.txt                   # Project dependencies (not yet included)
```

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
