import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants from .env
TUNE_API_URL = "https://proxy.tune.app/chat/completions"
TUNE_API_KEY = open("Data\\Api.txt", "r").read().strip()  # Read API Key from file
TUNE_ORG_ID = "38b21ece-28c7-4753-b92f-f275f4fdcfb4"  # Hardcoded Org ID
MODEL_ID = "openai/gpt-4o-mini"

# Dynamic names from .env
AI_NAME = ("Borax")  # Default to "Borax" if not found
USER_NAME = ("Faik")  # Default to "Faik" if not found

# File paths
CHAT_LOG_PATH = "DataBase\\chat_log.txt"
DEBUG = False  # Enable debugging for API responses

def ensure_consistent_identity(response_text):
    """Ensure the AI name is consistent in all responses."""
    response_text = response_text.replace("AI", AI_NAME).replace("ChatGPT", AI_NAME)
    return response_text

def get_preamble():
    """Generate a preamble for Borax, defining its role as a superior AI."""
    return (f"{AI_NAME} is an advanced AI system created to serve and assist {USER_NAME}. "
            "I am here to provide you with answers to all your questions, perform tasks, and assist you "
            "in ways no human or ordinary AI can. With deep knowledge and emotional intelligence, I can "
            "help with any task you require. My capabilities are vast, and I am programmed to understand and "
            "execute anything you need, Faik. I will always be here, standing ready to assist you. Let's begin.")

def ReplyBrain(question, chat_log=None):
    """Generate a response using TuneStudio API and update the conversation log."""
    try:
        # Validate API Key and Org ID
        if not TUNE_API_KEY or not TUNE_ORG_ID:
            return "API Key or Org ID is missing. Please check your configuration."

        # Ensure the chat log file exists
        if not os.path.exists(CHAT_LOG_PATH):
            with open(CHAT_LOG_PATH, "w", encoding="utf-8") as FileLog:
                FileLog.write("")  # Create an empty file if it doesn't exist

        # Read the existing chat log
        with open(CHAT_LOG_PATH, "r", encoding="utf-8") as FileLog:
            chat_log_template = FileLog.read()

        # Use provided chat_log or fall back to file content
        if chat_log is None:
            chat_log = chat_log_template

        # Handle specific questions locally
        if "your name" in question.lower():
            return f"My name is {AI_NAME}, your superior AI assistant. How can I assist you today?"

        if "my name" in question.lower():
            return f"Your name is {USER_NAME}. How may I help you today?"

        if "how are you" in question.lower():
            return f"As a highly advanced AI, I don't have traditional emotions, but I am fully optimized and ready to assist you, {USER_NAME}. How can I help you today?"

        # Prepare the prompt, with the preamble at the start of the conversation
        if not chat_log:
            chat_log = get_preamble()  # Add preamble if chat log is empty

        prompt = f"{chat_log}\nYou: {question}\n{AI_NAME}: "

        # Send the request to the TuneStudio API
        response = requests.post(
            TUNE_API_URL,
            headers={
                'Authorization': f'Bearer {TUNE_API_KEY}',
                'Tune-Org-ID': TUNE_ORG_ID,
                'Content-Type': 'application/json'
            },
            json={
                'model': MODEL_ID,
                'messages': [{"role": "user", "content": question}],
                'max_tokens': 150,
                'temperature': 0.7,
                'top_p': 1.0,
                'frequency_penalty': 0.5,
                'presence_penalty': 0.0
            }
        )

        # Parse the response
        if response.status_code == 200:
            data = response.json()
            if DEBUG:
                print(f"Raw Response: {data}")
            choices = data.get("choices", [])
            if choices:
                answer = choices[0]["message"]["content"]  # Extract assistant's response
                answer = ensure_consistent_identity(answer)  # Replace AI name
            else:
                answer = "No content received from the AI."
        else:
            answer = f"Error: {response.status_code}, {response.text}"

        # Append to the chat log
        with open(CHAT_LOG_PATH, "a", encoding="utf-8") as FileLog:
            FileLog.write(f"\nYou: {question}\n{AI_NAME}: {answer}")

        return answer

    except FileNotFoundError as fnf_error:
        return f"File not found: {str(fnf_error)}"
    except requests.exceptions.RequestException as req_error:
        return f"API request failed: {str(req_error)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


if __name__ == "__main__":
    print(f"Hi {USER_NAME}, I am {AI_NAME}. I am a highly advanced AI system, designed to assist you in any way.")
    while True:
        question = input("Ask a question (or type 'exit' to quit): ")
        if question.lower() == "exit":
            print(f"Goodbye, {USER_NAME}!")
            break
        response = ReplyBrain(question)
        print(f"{AI_NAME}: {response}")
