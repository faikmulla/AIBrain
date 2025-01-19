def system_control(command):
    try:
        controls = {
            "mute": lambda: keyboard.press_and_release("volume mute"),
            "unmute": lambda: keyboard.press_and_release("volume mute"),
            "volume up": lambda: keyboard.press_and_release("volume up"),
            "volume down": lambda: keyboard.press_and_release("volume down"),
        }
        if command in controls:
            controls[command]()
            return f"System command executed: {command}"
        else:
            return f"Invalid system command: {command}"
    except Exception as e:
        return f"Error executing system command '{command}': {e}"

# Weather Functionality
def get_weather(query=""):
    """
    Fetch weather information using OpenWeatherMap API.
    If no valid city is found in the query, default to Miraj, Maharashtra for generic queries.
    """
    API_KEY = "2060cf9d21ecd23b5f5d2c7f784ac42b"
    query = query.lower().replace("weather", "").strip()  # Remove 'weather' from the query

    # Default city for generic queries
    city = "Miraj,Maharashtra" if "update" in query or not query else query

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for non-200 responses
        weather_data = response.json()

        # Parse and format the weather data
        weather_desc = weather_data["weather"][0].get("description", "No description available").capitalize()
        temp = weather_data["main"].get("temp", "N/A")
        feels_like = weather_data["main"].get("feels_like", "N/A")
        humidity = weather_data["main"].get("humidity", "N/A")
        wind_speed = weather_data["wind"].get("speed", "N/A")

        return (
            f"Sir, the weather in {city.capitalize()}:\n"
            f"{weather_desc}\n"
            f"Temperature: {temp}°C, Feels like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s."
        )
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather: {str(e)}"

# News Functionality
def get_news(topic="latest", max_articles=5):
    if not NEWS_API_KEY:
        return "News API key is missing. Please set it in your environment variables."

    topic = topic.strip() or "latest"
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])
        if not articles:
            return f"No news articles found for the topic '{topic}'."

        top_articles = articles[:max_articles]
        return "\n\n".join(
            [
                f"{idx + 1}. {article.get('title', 'No Title')} - {article.get('description', 'No Description')} "
                f"(Source: {article.get('source', {}).get('name', 'Unknown Source')})\n"
                f"Read more: {article.get('url', 'No URL Available')}"
                for idx, article in enumerate(top_articles)
            ]
        )
    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"

# Command Execution
async def execute_command(command):
    command = command.strip()
    if command.startswith("open "):
        result = open_app(command.removeprefix("open ").strip())
    elif command.startswith("close "):
        result = close_app(command.removeprefix("close ").strip())
    elif command.startswith("play "):
        result = youtube_search(command.removeprefix("play ").strip())
    elif command.startswith("google search "):
        result = google_search(command.removeprefix("google search ").strip())
    elif command.startswith("system "):
        result = system_control(command.removeprefix("system ").strip())
    elif command.startswith("weather "):
        result = get_weather(command.removeprefix("weather ").strip())
    elif command.startswith("news "):
        result = get_news(command.removeprefix("news ").strip())
    else:
        return f"No feature found for command: {command}"
    return result

# Execute Multiple Commands
async def automate(commands):
    tasks = [execute_command(command) for command in commands]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            print(f"[red]Error:[/red] {result}")
        else:
            print(f"[green]{result}[/green]")

# Main Entry Point
# if __name__ == "__main__":
#     user_commands = [
#         "news latest",
#         "open chrome",
#         "weather Pune",
#         "system mute"
#     ]
#     asyncio.run(automate(user_commands))
