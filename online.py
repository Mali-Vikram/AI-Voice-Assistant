from ipaddress import ip_address

import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
# from decouple import config

EMAIL = ""
PASSWORD = ""



def find_my_ip():
    ip_addres= requests.get('https://api.ipify.org?format=json').json()
    return ip_addres["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences = 2)
    return results

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.playonyt(video)

def send_email(receiver_add, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['Subject'] = subject
        email['From'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True

    except Exception as e:
        print(e)
        return False

def get_news():
    news_headline = []
    result = requests.get(f"https://newsapi.org/v2/top-headlines?country=india&category=general&apiKey=48d2430761d641c5a3181de06b384339").json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:6]

def weather_forecast(city):
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=e7818cf8e041c3c12a646c368e384d77"
    ).json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temp}C", f"{feels_like}C"

