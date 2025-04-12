import os
import dspy
from fastapi import FastAPI, Body
from pydantic import BaseModel
from contextlib import asynccontextmanager

#
# Define a simple DSPy Signature
class MultiServerSignature(dspy.Signature):
    """Helpful Assistant with Tools Available"""
    history: list[dict[str, str]] = dspy.InputField(desc="The conversation history.")
    user_input: str = dspy.InputField(desc="The user's request, potentially requiring external tools.")
    output: str = dspy.OutputField(desc="The final response to the user should be in nueral language markdown format.")


# Define request model
class QueryRequest(BaseModel):
    query: str = "Hello, how can I help you?"

# Initialize global variables for reuse
lm = None
server_manager = None
react_agent = None

history = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the FastAPI application.
    
    This function handles startup and shutdown events:
    - On startup: Initializes the language model, MCP server manager, and reactive agent
    - On shutdown: Cleans up resources by closing connections
    """
    global lm, server_manager, react_agent
    
    # Startup: Initialize resources
    print("Starting up MCP API server...")
    
    # Initialize language model
    lm = dspy.LM("gemini/gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))
    # lm = dspy.LM("ollama/qwen2.5:14b-instruct")
    dspy.configure(lm=lm)
    print("Language model initialized")

    # Set up MCP Server Manager
    server_manager = dspy.MCPServerManager()
    config_path = r"backend/servers_config.json"
    config = server_manager.load_config(config_path)
    await server_manager.initialize_servers(config)
    print("MCP Server Manager initialized")
    print(f"Available servers: {server_manager.servers}")
    
    # Initialize reactive agent with all available tools
    all_mcp_tools = await server_manager.get_all_tools()
    print(f"Available tools: {all_mcp_tools}")
    print(len(all_mcp_tools), "tools available")
    react_agent = dspy.ReAct(
        MultiServerSignature,
        tools=all_mcp_tools,
        max_iters=7
    )
    print("Reactive agent initialized")
    
    # Yield control back to FastAPI
    yield
    
    # Shutdown: Clean up resources
    print("Shutting down MCP API server...")
    await server_manager.cleanup()
    
    # Additional cleanup if needed
    print("Shutdown complete")

# Create FastAPI app with the lifespan manager
app = FastAPI(
    title="MCP API", 
    description="API for MCP JIRA server", 
    version="0.1.0",
    lifespan=lifespan
)

@app.post("/mcp/query")
async def process_query(request: QueryRequest = Body(...)):
    """Process a query using the MCP server."""
    global history, react_agent
    try:
        result = await react_agent.async_forward(user_input=request.query, history=history)
        history.append({"role": "user", "content": request.query})
        history.append({"role": "assistant", "content": result.output})
        return {"result": result.output}
    except Exception as e:
        return {"error": str(e)}

# For running with uvicorn in reload mode for real-time updates
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)