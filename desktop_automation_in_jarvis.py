import pywhatkit
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
from time import sleep
import os
from datetime import timedelta
import random
from plyer import notification
import pyautogui
import wikipedia
import smtplib
import user_config  # Make sure this has gmail_user and gmail_password
import openai_request as ai
import mtranslate
import requests

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    if audio:
        try:
            # Optional: accent/locale translation
            audio = mtranslate.translate(audio, to_language="en", from_language="en-in")
        except Exception:
            pass  # fallback to original if translation fails
        print(f"Jarvis: {audio}")
        engine.say(audio)
        engine.runAndWait()
    else:
        print("No audio to speak.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query
    except Exception as e:
        print("Could not understand. Please say that again.")
        return None

def send_email():
    speak("Please provide the recipient's email address.")
    recipient_email = takeCommand()
    if recipient_email is None:
        speak("No recipient email provided.")
        return

    speak("What is the subject of the email?")
    subject = takeCommand()
    if subject is None:
        speak("No subject provided.")
        return

    speak("What is the message content?")
    message = takeCommand()
    if message is None:
        speak("No message content provided.")
        return

    try:
        pywhatkit.send_mail(user_config.gmail_user, user_config.gmail_password, subject, message, recipient_email)
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"An error occurred: {str(e)}")

def open_app(query):
    app_name = query.replace("open", "").replace("jarvis", "").strip()
    if app_name:
        speak(f"Opening {app_name}")
        pyautogui.press("super")  # Windows key
        pyautogui.typewrite(app_name)
        pyautogui.sleep(2)
        pyautogui.press("enter")
    else:
        speak("Please specify the application name.")

def main_process():
    while True:
        request = takeCommand()
        if request is None:
            continue

        query = request.lower()

        if "hello" in query:
            speak("Welcome, how can I help you.")

        elif "send email" in query:
            send_email()

        elif "open" in query:
            open_app(query)

        elif "exit" in query or "quit" in query:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main_process()
