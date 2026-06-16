import os
from dotenv import set_key

# --- Configuration ---
ENV_FILE_PATH = ".env"
KEY_NAME = "GEMINI_API_KEY"

def setup_environment():
    """
    Prompts the user for the Gemini API Key and securely saves it to a .env file.
    """
    print("--- 🩺 Medical AI Chatbot Setup ---")
    print("This script will create a '.env' file to store your API key securely.")
    
    # Check if .env file already exists
    if os.path.exists(ENV_FILE_PATH):
        print(f"\n⚠️ The {ENV_FILE_PATH} file already exists.")
        with open(ENV_FILE_PATH, 'r') as f:
            content = f.read()
            if KEY_NAME in content:
                print(f"The '{KEY_NAME}' appears to be present. Skipping key entry.")
                return

    # Prompt the user for the key
    api_key = input(f"\nPlease enter your Google Gemini API Key: ")
    
    if not api_key:
        print("\n❌ API Key cannot be empty. Setup aborted.")
        return
        
    try:
        # Use set_key to write or update the key in the .env file
        set_key(ENV_FILE_PATH, KEY_NAME, api_key)
        
        print("\n✅ Success!")
        print(f"The environment variable '{KEY_NAME}' has been saved to the {ENV_FILE_PATH} file.")
        print("Run 'streamlit run app.py' to start the chatbot.")

    except Exception as e:
        print(f"\n❌ An error occurred while writing the file: {e}")

if __name__ == "__main__":
    setup_environment()