# from ipaddress import ip_address
# from multiprocessing.managers import view_type
from enum import nonmember

import pyttsx3
import requests
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
# import imdb
import wolframalpha
import pyautogui
from datetime import datetime
# from decouple import config
from random import choice
from conv import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast
from pyexpat.errors import messages

engine = pyttsx3.init('sapi5')
engine.setProperty('volume',1.5)
engine.setProperty('rate',225)
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id) # 0:male  1:female

USER = "VIKRAM"
HOSTNAME = "JARVIS"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USER}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good Afternoon {USER}")
    elif (hour >= 16) and (hour <= 19): # 19 -> 19:59
        speak(f"Good Evening {USER}")
    else:
        speak(f"Good Time {USER}")
    speak(f"I am {HOSTNAME}. How may I assist you?")

listening = False

def start_listening():
    global listening
    listening = True
    print("Started Listening ")

def pause_listening():
    global listening
    listening = False
    print("stopped listening")

keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        queri= r.recognize_google(audio)
        print(queri)
        if not 'stop' in queri or 'exit' in queri or 'escape' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if (hour >= 21) and (hour < 6):
                speak(f"Good night {USER}, take care!")
            else:
                speak(f"Have a Good Day {USER}!")
            exit()

    except Exception:
        speak("Sorry I couldn't understand. Can you please repeat that?")
        queri = 'None'
    return queri



if __name__ == '__main__':
    # speak("Hii I am a virtual assistance")
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine sir, What about you?")
            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening Camera")
                sp.run('start microsoft.windows.camera:', shell = True)

            elif "open notepad" in query:
                speak("Opening Notepad")
                notepad_path = "C:\\Users\\LENOVO\\Downloads\\NoteGPT_BUILD AN AI ASSISTANT WITH PYTHON_ JARVIS-INSPIRED PROJECT.txt"
                os.startfile(notepad_path)

            elif "open discord" in query:
                speak("Opening Discord")
                discord_path = "C:\\Users\\LENOVO\\OneDrive\\Desktop\\Discord.lnk"
                os.startfile(discord_path)

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(f"your ip address is {ip_address}")
                print(f"your ip address is {ip_address}")

            elif "open youtube" in query:
                speak("What do you want to play on youtube? ")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak("What do you want to search on Google? ")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("What do you want to search on Wikipedia? ")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to Wikipedia, {results}")
                speak("I am printing it in terminal")
                print(results)

            elif "send an email" in query:
                speak("On what email address do you want to send ? Please enter in the Terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject ?")
                subject = take_command().capitalize()
                speak("What is the message? ")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email ")
                    print("Email has been sent.")
                else:
                    speak("Something went wrong, Please check the error Log...")

            elif "give me news" in query:
                speak(f"I am reading out the latest headlines of today")
                speak(get_news())
                speak("I am printing down")
                print(*get_news(), sep='\n')

            elif "weather" in query:
                ip_address = find_my_ip()
                speak(f"Tell me the name of your city")
                city = input("Enter name of your city: ")
                speak(f"Getting weather report of your city{city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The Current temperature is {temp}, but it feels like{feels_like}")
                speak(f"Also the weather report talks about {weather}")
                speak("For your convenience, I am printing it on the screen sir.")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

            # elif "movie" in query:
            #     movies_db = imdb.IMDb()
            #     speak("Please tell me the movie name:")
            #     text = take_command()
            #     movies = movies_db.search_movie(text)
            #     speak("Searching for" + text)
            #     speak("I found these ")
            #     for movie in movies:
            #         title = movie["title"]
            #         year = movie["year"]
            #         speak(f"{title}-{year}")
            #         info = movie.getID()
            #         movie_info = movies_db.get_movie(info)
            #         rating = movie_info["rating"]
            #         cast = movie_info["cast"]
            #         actor = cast[0:5]
            #         plot = movie_info.get("plot","plot summary not available")
            #         speak(f"{title} was released in {year} has imdb ratings of {rating}. It has a cast of {actor}. The plot summary of movie is {plot}.")
            #         print(f"{title} was released in {year} has imdb ratings of {rating}. It has a cast of {actor}. The plot summary of movie is {plot}.")

            elif "calculate" in query:
                app_id = "5K7X59-GY63EVXH6X"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                except StopIteration:
                    speak("I couldn't find that. Please try again")

            elif "What is" in query or "who is" in query or"which is"in query:
                app_id = "5K7X59-GY63EVXH6X"
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index("what is") if "what is" in query.lower() else \
                        query.lower().index("who is") if "who is" in query.lower() else \
                        query.lower().index("which is") if "which is" in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind+2:]
                        result = client.query(" ".join(text))
                        ans = next(result.results).text
                        speak("The answer is " + ans)
                        print("The answer is " + ans)
                    else:
                        speak("I couldn't find that.")

                except StopIteration:
                    speak("I couldn't find that, please try again...")

            elif "subscribe" in query:
                break

            else:
                pass      #    ------------>>>>>>>>>------------->>>>>>>>>>------------>>>>>>>>>-----------------------------------------------------------
            
            # Can enter API key form Open AI and can get answer of any question .
            # But it is not free and it is paid service. So we are not using it here
            # And can also make the answer's came out to be printed as {JARVIS: "answer"} and then use speak method just for "answer".




           