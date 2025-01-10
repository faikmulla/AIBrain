import cohere
import os
import datetime

COHERE_API_KEY = os.getenv('COHERE_API_KEY', 'Your_cohere_API_key')
co = cohere.Client(COHERE_API_KEY)

user_name = "Your_name"
AI_Assistant = "Borax"
conversation_history = []

def get_greeting():
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        return "Good morning"
    elif current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def update_conversation_log(user_input, bot_response):
    conversation_history.append(f"You: {user_input}")
    conversation_history.append(f"Borax: {bot_response}")

def personalize_response(response):
    response = response.replace("User", user_name)
    return response

def search_chat_log(query):
    if os.path.exists("Database/chat_log.txt"):
        with open("Database/chat_log.txt", "r", encoding="utf-8") as file:
            chat_log = file.readlines()
        for i in range(len(chat_log) - 1, 0, -2):
            user_input = chat_log[i - 1].strip().lower()
            if query.lower() in user_input:
                return chat_log[i].strip().replace("Borax:", "").strip()
    return None

def modify_response_based_on_style(response, style):
    if style == "friendly":
        return f"Hey there! {response} 😊"
    elif style == "formal":
        return f"Good day, {user_name}. {response} I remain at your service."
    elif style == "sarcastic":
        return f"Oh, sure! {response} 🙄 But, like, who wouldn't want that, right?"
    else:
        return response

def ReplyBrain(question, chat_log=None, style="neutral"):
    previous_response = search_chat_log(question)
    if previous_response:
        return modify_response_based_on_style(previous_response, style)

    if 'hello' in question.lower() or 'hi' in question.lower():
        greeting = get_greeting()
        return modify_response_based_on_style(f"{greeting}, {user_name}! How can I assist you today?", style)

    if not chat_log:
        chat_log = "\n".join(conversation_history)

    prompt = f"{chat_log}\nYou: {question}\nBorax:"

    try:
        response = co.generate(
            model="command-xlarge",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
            frequency_penalty=0.5,
            presence_penalty=0.5
        )

        bot_response = response.generations[0].text.strip()
        bot_response = personalize_response(bot_response)
        bot_response = modify_response_based_on_style(bot_response, style)
        update_conversation_log(question, bot_response)

        with open("Database/chat_log.txt", "a", encoding="utf-8") as file:
            file.write(f"You: {question}\nBorax: {bot_response}\n\n")

        return bot_response

    except Exception as e:
        return f"An error occurred: {e}"

def real_time_conversation():
    print("Borax: Ready to chat! Ask me anything or say 'exit' to stop.")
    
    while True:
        style = input("Choose response style (friendly, formal, sarcastic, neutral): ").lower()
        user_input = input(f"You ({user_name}): ")

        if user_input.lower() == "exit":
            print("Borax: Goodbye, have a great day!")
            break

        response = ReplyBrain(user_input, style=style)
        print(f"Borax: {response}")

if __name__ == "__main__":
    real_time_conversation()
