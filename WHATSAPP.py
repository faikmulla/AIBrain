import datetime
import pywhatkit as kit
import keyboard
import time
import pygetwindow as gw
import pyautogui

def send_whatsapp_message(phone_no, message):
    """
    Sends a WhatsApp message to the specified phone number in the background.
    """
    try:
        # Get current time
        now = datetime.datetime.now()
        print(f"Current time: {now.hour}:{now.minute}")

        # Schedule the message 2 minutes from now
        future_time = now + datetime.timedelta(minutes=2)
        time_hour = future_time.hour
        time_min = future_time.minute

        print(f"Scheduling message for {time_hour}:{time_min}")

        # Send WhatsApp message
        kit.sendwhatmsg(
            phone_no=+919421198981,  # Replace with recipient's phone number
            message=message,
            time_hour=time_hour,
            time_min=time_min,
            wait_time=10  # Adjust wait time as needed
        )

        # Wait for WhatsApp Web to load and the message to be typed
        time.sleep(15)  # Adjust delay based on your system/browser speed

        # Bring the browser window to the front
        whatsapp_window = None
        for window in gw.getWindowsWithTitle('WhatsApp'):
            whatsapp_window = window
            break

        if whatsapp_window:
            whatsapp_window.activate()  # Focus the WhatsApp Web browser window
            time.sleep(1)  # Small delay to ensure the window is active

        # Simulate pressing the "Enter" key
        keyboard.press_and_release("enter")  # Use keyboard to press "Enter"
        print("Message sent!")

        # Wait a few seconds before closing the browser
        time.sleep(5)  # Adjust this time if necessary

        # Close the WhatsApp browser window
        if whatsapp_window:
            pyautogui.hotkey('ctrl', 'w')  # Use 'ctrl + w' to close the window
            print("Browser closed!")
    except Exception as e:
        print(f"An error occurred: {e}")
