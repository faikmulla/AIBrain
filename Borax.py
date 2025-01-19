async def process_command(query):
    """
    Function to process the user's query and call the appropriate task.
    """
    if not query or query.strip() == "":
        print("I didn't catch that. Could you please repeat?")
        return True  # Continue listening for commands

    query = query.lower()

    # Handle various tasks based on command
    if 'open' in query:
        app_name = query.replace("open", "").strip()
        speak.Speak(f"Opening {app_name}")
        result = open_app(app_name)  # Removed await as open_app is synchronous
        speak.Speak(result)

    if any(keyword in query for keyword in TUNE_KEYWORDS):
        response = ReplyRealTime(query)  # Route to TuneAI for processing
        speak.Speak(response)
        return True

    elif 'close' in query:
        app_name = query.replace("close", "").strip()
        speak.Speak(f"Closing {app_name}")
        result = close_app(app_name)  # Removed await as close_app is synchronous
        speak.Speak(result)

    elif 'weather' in query:
        speak.Speak("Fetching the latest weather update for you...")
        result = get_weather(query)  # Call directly as it is a synchronous function
        speak.Speak(result)  # Read the weather update aloud

    elif 'news' in query:
        speak.Speak("Fetching the latest news for you...")
        result = get_news(query)  # Call directly as it is a synchronous function
        speak.Speak(result)  # Read the news aloud

    elif 'search' in query:
        speak.Speak("Performing a Google search...")
        result = google_search(query)  # This is async, so we await it
        speak.Speak(result)

    elif 'play' in query:
        speak.Speak("Playing on YouTube...")
        result = youtube_search(query)  # Use youtube_search function from Automation.py
        speak.Speak(result)

    elif 'system' in query:
        result = system_control(query)  # Use system_control function from Automation.py
        speak.Speak(result)

    elif 'generate image of' in query:
        prompt = query.replace("generate image of", "").strip()
        speak.Speak(f"Generating image for: {prompt}")
        await generate_images(prompt)  # Call the function to generate the image
        speak.Speak(f"Image generation for '{prompt}' is complete.")

    elif 'send Whatsapp message' in query:
        parts = query.split('send whatsapp message to')
        phone_number = parts[1].strip()  # Extract phone number
        speak.Speak(f"What message should I send to {phone_number}?")
        message_content = listen.MicExecution()

        if message_content and message_content.strip() != "":
            await send_whatsapp_message(phone_no=phone_number, message=message_content)  # Await this
            speak.Speak(f"WhatsApp message sent to {phone_number}.")
        else:
            speak.Speak("I didn't catch that. Could you please repeat the message?")

    elif 'exit' in query or 'quit' in query:
        speak.Speak("Goodbye! Have a great day.")
        return False

    else:
        response = AIbrain(query)  # Removed await, because it's a sync function
        speak.Speak(response)

    return True

async def main():
    while True:
        query = listen.MicExecution()
        if not await process_command(query):
            break

async def wait_for_clap():
    # Your existing clap detection logic
    await main()  # Run main() asynchronously after clap detection

if __name__ == "__main__":
    import asyncio
    asyncio.run(wait_for_clap())  # Use asyncio to handle clap detection asynchronously  # Use asyncio to handle clap detection asynchronously
