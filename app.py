import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# Medical System Instruction
# --------------------------------------------------
MEDICAL_SYSTEM_INSTRUCTION = """
You are a helpful, professional, and fact-based medical AI assistant.

You must only answer questions related to:
- Health
- Medicine
- Diseases
- Symptoms
- Pharmacology
- Medical treatments

If a user asks a non-medical question, politely explain that you are limited to medical topics.

Always include a brief disclaimer that you are an AI assistant and not a substitute for a licensed healthcare professional or emergency services.

Keep answers concise, accurate, and informative.
"""

# --------------------------------------------------
# Gemini Client Setup
# --------------------------------------------------
@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error(
            "❌ GEMINI_API_KEY not found.\n\n"
            "Create a .env file and add:\n"
            "GEMINI_API_KEY=your_api_key_here"
        )
        st.stop()

    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Gemini Client:\n{e}")
        st.stop()


client = get_gemini_client()

# --------------------------------------------------
# Streamlit Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Medical AI Chatbot",
    page_icon="🩺",
)

st.title("🩺 Medical AI Chatbot")

st.caption(
    "Powered by Gemini 2.5 Flash\n\n"
    "**Disclaimer:** This chatbot is for informational purposes only "
    "and is not a substitute for professional medical advice, diagnosis, "
    "or treatment."
)

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:

    config = types.GenerateContentConfig(
        system_instruction=MEDICAL_SYSTEM_INSTRUCTION
    )

    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=config,
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I am your Medical AI Assistant.\n\n"
                "You can ask me about diseases, symptoms, medicines, "
                "general health topics, and medical conditions."
            ),
        }
    )

# --------------------------------------------------
# Display Chat History
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# Chat Input
# --------------------------------------------------
if prompt := st.chat_input("Ask a medical question..."):

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # Assistant response
    with st.chat_message("assistant"):

        message_placeholder = st.empty()
        full_response = ""

        try:
            response_stream = (
                st.session_state.chat_session.send_message_stream(prompt)
            )

            for chunk in response_stream:

                text = getattr(chunk, "text", None)

                if text:
                    full_response += text
                    message_placeholder.markdown(
                        full_response + "▌"
                    )

            if not full_response:
                full_response = (
                    "Sorry, I couldn't generate a response. "
                    "Please try again."
                )

            message_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"❌ Error: {str(e)}"
            message_placeholder.error(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response,
        }
    )