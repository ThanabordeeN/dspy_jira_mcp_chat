import streamlit as st
import requests

st.title("JIRA MCP Chatbot")

# Initialize session state for storing conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

def send_request(prompt_text):
    try:
        # Format the prompt as expected by the API
        payload = {"query": prompt_text}
        response = requests.post("http://localhost:8001/mcp/query", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

# Display chat history from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask a question about your JIRA tickets")

# Process new messages
if prompt:
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Show a spinner while waiting for the response
    with st.spinner("Thinking..."):
        response = send_request(prompt)
    
    # Display assistant response
    if response:
        assistant_response = response.get("result", "No result found in response")
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
