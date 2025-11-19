import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pyjokes
import os

#  GLOBAL TTS ENGINE

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[0].id)

#  SPEAK FUNCTION

def speak(text):
    print("🧠 Victor:", text)
    engine.say(text)
    engine.runAndWait()

#  TRAIN NLP MODEL

commands = [
    "what is the time", "tell me the time", "current time",
    "open youtube", "play video on youtube", "start youtube",
    "search wikipedia", "find info on wikipedia", "tell me about",
    "search google", "find on google", "look up online",
    "tell me a joke", "make me laugh", "say something funny", "feeling boring today",
    "exit program", "quit", "bye"
]

labels = [
    "time", "time", "time",
    "youtube", "youtube", "youtube",
    "wikipedia", "wikipedia", "wikipedia",
    "google", "google", "google",
    "joke", "joke", "joke", "joke",
    "exit", "exit", "exit"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(commands)
model = LogisticRegression()
model.fit(X, labels)

#  FUNCTIONS

def get_intent(command):
    x = vectorizer.transform([command])
    return model.predict(x)[0]

def open_any_app(command):
    command = command.lower()
    app_paths = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "file explorer": "explorer.exe",
        "wordpad": "write.exe",
    }

    for app, path in app_paths.items():
        if app in command:
            try:
                os.startfile(path)
                speak(f"Opening {app}")
                return
            except Exception:
                speak(f"Sorry, I couldn’t open {app}.")
                return

    speak("Sorry, I don't know how to open that app yet.")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎧 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        print("🗣️ You:", query)
        return query.lower()
    except Exception:
        speak("Sorry, I didn’t catch that.")
        return ""

def process_command(command):
    if not command:
        return

    if "open" in command:
        if "youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            return
        elif "google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
            return
        elif "wikipedia" in command:
            speak("Opening Wikipedia")
            webbrowser.open("https://www.wikipedia.org")
            return
        else:
            open_any_app(command)
            return

    intent = get_intent(command)

    if intent == "time":
        time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {time}")

    elif intent == "youtube":
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif intent == "wikipedia":
        speak("Searching Wikipedia...")
        query = command.replace("search", "").replace("wikipedia", "")
        try:
            result = wikipedia.summary(query, sentences=2)
            print("\n📘 Wikipedia:", result)
            speak(result)
        except Exception:
            speak("Sorry, I couldn’t find any result on Wikipedia.")

    elif intent == "google":
        speak("What should I search for?")
        query = take_command()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak("Here are the search results.")

    elif intent == "joke":
        joke = pyjokes.get_joke()
        speak(joke)

    elif intent == "exit":
        speak("Goodbye!")
        exit()

    else:
        speak("Sorry, I didn’t understand that command.")

#  HOTWORD DETECTION

def listen_for_hotword():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n👂 Waiting for 'Hey Victor'...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in').lower()
        print("Heard:", query)

        if "hey victor" in query:
            speak("Yes, I'm listening...")
            command = take_command()
            process_command(command)

    except Exception:
        pass

#  MAIN LOOP

speak("Hey buddy! Victor is online and listening for 'Hey Victor'.")

while True:
    listen_for_hotword()

