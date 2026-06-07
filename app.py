import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load the hidden API key from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini Client
client = genai.Client(api_key=api_key)

# App layout
st.title("🚀 Personal AI OS: The Idea Hopper")
st.write("Dump your raw thoughts, fragments, or tasks below. Your AI partner will categorize and structure them instantly.")

# User Input Box
user_brain_dump = st.text_area("What's on your mind?", placeholder="e.g., Remind me to water the plants tomorrow at 4pm, also I think a solar-powered coffee mug would be a funny invention...")

if st.button("Hop Into System"):
    if user_brain_dump.strip() == "":
        st.warning("Please type something first!")
    elif not api_key:
        st.error("API Key missing! Check your .env file.")
    else:
        with st.spinner("Processing your thoughts..."):
            # The System Instruction that turns Gemini into a data sorter
            system_instruction = (
                "You are the central parsing core of a Personal AI Operating System. "
                "Your job is to take raw, chaotic thoughts and sort them into a clean, "
                "structured Markdown format. Group items into categories like [Tasks], "
                "[Project Ideas], or [Random Logs]. Be concise."
            )
            
            try:
                # Call the lightweight and fast Gemini 2.5 Flash model
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_brain_dump,
                    config={"system_instruction": system_instruction}
                )
                
                # Show the output on the screen
                st.success("Parsed Successfully!")
                st.markdown("### 📥 Sorted Output")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")