# Import necessary libraries
import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import pyttsx3
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Initialize chat string
chatStr = ""

# Function to convert text to speech


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to handle chat with OpenAI


def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"Bhavesh: {query}\n Hunter: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"][0]["text"].strip())
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text'].strip()}\n"
    return response["choices"][0]["text"]

# Function to handle AI responses


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

# Function to take voice commands


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Hunter"


# Initialize user input type
user_input_type = None

# Function to get user input


def get_user_input():
    global user_input_type
    if user_input_type is None:
        user_input_type = input(
            "Please choose input type: 1 for speech, 2 for text: ").strip()
    if user_input_type == "1":
        return takeCommand().lower()
    elif user_input_type == "2":
        return input("Please enter your command: ").lower()
    else:
        print("Invalid input type. Please enter 1 for speech or 2 for text.")
        user_input_type = None
        return get_user_input()

# Main function
if __name__ == '__main__':
    # Initial greetings
    print('Welcome to Hunter AI, How are you doing today?')
    say("Welcome to Hunter AI...")
    say("How are you doing today?")

    # Main loop
    while True:
        print("Listening...")
        query = get_user_input()  # Get user input

        # List of sites to open
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia",
                                                          "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        # Check if user wants to open a site
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])  # Open the site

        # Check if user wants to set volume
        if "set volume to" in query:
            try:
                # Extract volume percentage from query
                vol_percentage = int(query.split("set volume to")[1].strip())
                volume.SetMasterVolumeLevelScalar(
                    vol_percentage / 100, None)  # Set volume
                say(f"Volume set to {vol_percentage} percent")
            except Exception as e:
                say("Sorry, I couldn't set the volume. Please try again.")

        # Check if user wants to set brightness
        if "brightness" in query:
            try:
                # Extract brightness percentage from query
                brightness_percentage = int(
                    query.split("brightness to")[1].strip())
                sbc.set_brightness(brightness_percentage)  # Set brightness
                say(f"Brightness set to {brightness_percentage} percent")
            except Exception as e:
                say("Sorry, I couldn't set the brightness. Please try again.")

        # Check if user wants to open music
        if "open music" in query:
            musicPath = "E:/Unstoppable.mp3"
            os.system(f"start {musicPath}")  # Open the music

        # Check if user wants to use AI
        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        # Check if user wants to exit
        elif "exit".lower() in query.lower():
            say("It was nice to talk to you, see you soon!")
            exit()

        # Check if user wants to reset chat
        elif "reset chat".lower() in query.lower():
            chatStr = ""

        # If none of the above, start chatting
        else:
            print("Chatting...")
            chat(query)
