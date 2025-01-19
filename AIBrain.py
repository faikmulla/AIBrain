from groq import Groq
from json import load, dump, JSONDecodeError
import datetime
from dotenv import dotenv_values

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key
Username = "Your_name"
Assistantname = "Borax"
GroqAPIKey = "your_groq_api"

client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store messages
messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi**
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""
SystemBot = [
    {"role": "system", "content": System}
]

try:
    with open("DataBase/chat_log.json", "r") as f:
        content = f.read().strip()
        if content:
            f.seek(0)
            messages = load(f)
        else:
            print("The file is empty.")
except FileNotFoundError:
    with open("DataBase/chat_log.json", "w") as f:
        dump([], f)
except JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")

def Realtime():
    current_date_time = datetime.datetime.now()  # Get the current date and time.
    day = current_date_time.strftime("%A")  # Day of the week.
    date = current_date_time.strftime("%d")  # Day of the month.
    month = current_date_time.strftime("%B")  # Full month name.
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")  # Hour in 24-hour format.
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes:{second} seconds.\n"
    return data

def Clean_Answer(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def AIbrain(query):
    try:
        with open("DataBase/chat_log.json", "r") as f:
            content = f.read().strip()
            if content:
                f.seek(0)
                messages = load(f)
            else:
                print("The file is empty.")

        messages.append({"role": "user", "content": f"{query}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemBot + [{"role": "user", "content": Realtime()}] + messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</u>", "")

        messages.append({"role": "assistant", "content": Answer})

        with open("DataBase/chat_log.json", "w") as f:
            dump(messages, f, indent=4)

        return Clean_Answer(Answer=Answer)

    except Exception as e:
        print(f"An error occurred: {e}")
        with open("DataBase/chat_log.json", "w") as f:
            dump([], f, indent=4)
        return AIbrain(query)
