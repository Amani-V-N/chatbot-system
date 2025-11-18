import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI
from gtts import gTTS
import pygame
import time
import datetime

client = OpenAI(api_key="YOUR_API_KEY")
pygame.mixer.init()

def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("voice.mp3")
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

def listen():
    fs = 16000
    duration = 4
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write("input.wav", fs, audio)
    try:
        with open("input.wav", "rb") as f:
            text = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=f
            ).text
        return text
    except:
        return None

def check_custom(text):
    t = text.lower()
    if "tell me about st joseph college" in t or "tell me about st josph college" in t or "tell me about st joseph's college" in t:
        return ("St. Joseph’s College (Autonomous), Irinjalakuda, stands among the top 10 colleges in Kerala "
                "with a legacy of more than 60 years in delivering quality, value-based education for the holistic "
                "development of women. Recognized with an A++ NAAC accreditation, ranked 85th in NIRF 2024 and 83rd "
                "in NIRF 2025, the institution exemplifies excellence in academics, research, and student success. "
                "Ranked 7th in the KIRF rankings 2024, the college is celebrated for its commitment to holistic "
                "education, outstanding placements, and shaping the future of talented minds.")
    if "time now" in t or "what's the time" in t or "current time" in t:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."
    return None

def ask_gpt(text):
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Joseph AI, a friendly female humanoid robot."},
            {"role": "user", "content": text}
        ]
    )
    return r.choices[0].message.content

def robot_talk():
    while True:
        text = listen()
        if not text:
            continue
        if "exit" in text.lower():
            speak("Joseph AI is shutting down. Goodbye.")
            break
        custom = check_custom(text)
        if custom:
            speak(custom)
            continue
        reply = ask_gpt(text)
        speak(reply)

robot_talk()