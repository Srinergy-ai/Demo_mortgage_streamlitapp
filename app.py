import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Mortgage Assistant", page_icon="🏠")
st.title("🏠 Mortgage Underwriting Assistant")

# Configuration
# LANGFLOW_URL = os.getenv("LANGFLOW_URL")
# API_KEY = os.getenv("LANGFLOW_API_KEY")

LANGFLOW_URL = st.secrets["LANGFLOW_URL"]
API_KEY = st.secrets["LANGFLOW_API_KEY"]

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []

def extract_message_from_response(response_data):
    """
    Extract the bot's message from Langflow response
    Path: response['outputs'][0]['outputs'][0]['results']['message']['data']['text']
    """
    try:
        outputs = response_data.get('outputs', [])
        if outputs:
            inner_outputs = outputs[0].get('outputs', [])
            if inner_outputs:
                results = inner_outputs[0].get('results', {})
                message = results.get('message', {})
                data = message.get('data', {})
                text = data.get('text', '')
                
                if text:
                    return text
        
        return "No response received from the assistant."
    
    except (KeyError, IndexError, TypeError) as e:
        st.error(f"Error parsing response: {str(e)}")
        return "Error: Could not parse the response."

def call_langflow_api(user_message: str, session_id: str):
    """
    Send message to Langflow API
    """
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": user_message,
        "session_id": session_id
    }
    
    try:
        response = requests.post(
            LANGFLOW_URL, 
            json=payload, 
            headers=headers, 
            timeout=120
        )
        response.raise_for_status()
        return response.json(), None
    
    except requests.exceptions.Timeout:
        return None, "⏱️ Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "🔌 Could not connect to the server."
    except requests.exceptions.HTTPError as e:
        return None, f"❌ HTTP Error {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Ask me about mortgage underwriting..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyzing your request..."):
            response_data, error = call_langflow_api(user_input, st.session_state.session_id)
        
        if error:
            bot_message = error
            st.error(bot_message)
        else:
            bot_message = extract_message_from_response(response_data)
            st.markdown(bot_message)
    
    # Save bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_message})

# Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Session Controls")
    
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("## 📊 Session Info")
    st.code(st.session_state.session_id, language="text")
    st.metric("Total Messages", len(st.session_state.messages))
    
    st.markdown("---")
    
    st.markdown("## 💡 Example Questions")
    st.markdown("""
    - Can this FHA cash-out refinance be approved?
    - What's the DTI on this loan?
    - Do a red flag analysis for this file
    - What are the FHA seasoning rules?
    - Which programs accept a 604 FICO score?
    """)
    
    st.markdown("---")
    st.caption("Powered by Langflow 🚀")
