import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import psutil
import platform
import subprocess
import pywhatkit

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning, sir!")
    elif hour < 18:
        speak("Good afternoon, sir!")
    else:
        speak("Good evening, sir!")
    speak("Jarvis at your service. How can I help you?")

def open_application(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "command prompt": "cmd.exe",
    }
    if app_name in apps:
        subprocess.Popen(apps[app_name])
        speak(f"Opening {app_name}")
    else:
        speak("Application not found in my database.")

def get_system_info():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "Battery info not available"
    speak(f"CPU usage is at {cpu} percent")
    speak(f"Memory usage is at {memory} percent")
    speak(f"Battery is at {battery_percent} percent")

def process_command(command):
    command = command.lower()

    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com/")
    elif "play i nahin" in command:
        webbrowser.open("https://youtu.be/nFgsBxw-zWQ?si=vZyIUps9NK4kwvhf")
    elif "search" in command:
        speak("What should I search on Google?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        search_query = recognizer.recognize_google(audio)
        speak(f"Searching Google for {search_query}")
        pywhatkit.search(search_query)
    elif "open" in command:
        for app in ["notepad", "calculator", "paint", "command prompt"]:
            if app in command:
                open_application(app)
                break
    elif "system info" in command or "system information" in command:
        get_system_info()
    elif command == "say my name":
        speak("Hello, Mohit sir")
    elif command == "exit":
        speak("Goodbye sir. Shutting down Jarvis.")
        exit()

if __name__ == "__main__":
    speak("Jarvis initializing...")
    greet_user()
    while True:
        print("Listening...")
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {command}")

            if "jarvis" in command.lower():
                speak("Yes sir, how may I assist?")
            else:
                process_command(command)

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError:
            print("Network error. Please check your internet.")
        except Exception as e:
            print(f"Error: {e}")
