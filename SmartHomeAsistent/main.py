# pip install speechrecognition pyaudio transformers tiktoken sentencepiece torch tf-keras tensorflow pyserial gTTS pygame
import speech_recognition as sr  # za test koristi python -m speech_recognition
from transformers import pipeline
import time
from gtts import gTTS
import io
import pygame
import serial

NAREDBE = ["ugasiti svjetlo", "upaliti svjetlo", "kolika temperatura", "otvoriti vrata", "zatvoriti vrata"]


def izgovori(text):
    tts = gTTS(text=text, lang='hr')

    fp = io.BytesIO()  # napravimo datoteku gdje cemo spremiti zvuk
    tts.write_to_fp(fp)  # zapiseno zvuk koji generira text-to-speech
    fp.seek(0)  #vratimo se na pocetak datoteke

    # pustimo zvuk uz pomoc pygame biblioteke
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()


def obradiNaredbu(naredba):
    if naredba == 0:  # upaliti svijetlo
        arduinoSerial.write(bytes('0', 'utf-8'))
        izgovori("Ugasio sam svijetlo.")
    if naredba == 1:  # ugasiti svijetlo
        arduinoSerial.write(bytes('1', 'utf-8'))
        izgovori("Upalio sam svijetlo.")
    if naredba == 2:  # kolika temperatura
        arduinoSerial.write(bytes('2', 'utf-8'))
        time.sleep(0.1)
        temp = arduinoSerial.readline()
        izgovori("U prostoriji je " + temp.decode('utf-8') + " stupnjeva Celzijusa.")
    if naredba == 3:  # otvori vrata
        arduinoSerial.write(bytes('3', 'utf-8'))
    if naredba == 4:  # zatvori vrata
        arduinoSerial.write(bytes('4', 'utf-8'))

def klasicifirajNaredbu(text):
    result = classifier(text, candidate_labels=NAREDBE)

    label = result['labels'][0]
    score = result['scores'][0]

    print(label + " -> " + str(round(score * 100, 2)) + "%")

    if score >= 0.5:
        return NAREDBE.index(label)

    return -1


def prepoznataRecenica(text):
    if "marko" not in text.lower():
        return

    print("Cuo sam: " + text)
    naredba = klasicifirajNaredbu(text)

    if naredba == -1:
        izgovori("Oprosti, nisam razumio naredbu...")
    else:
        obradiNaredbu(naredba)


def cuoNesto(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio, language="hr-HR")
        prepoznataRecenica(text)
    except sr.RequestError:
        print("API ne radi!")
    except sr.UnknownValueError:
        pass


model_name = "joeddav/xlm-roberta-large-xnli"
classifier = pipeline("zero-shot-classification", model=model_name)

arduinoSerial = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

recognizer = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    recognizer.adjust_for_ambient_noise(source)  # prilagodavanje okolinskoj buki

listening = recognizer.listen_in_background(mic, cuoNesto)

print("--==========================--")
print("  SADA MOZES POCETI GOVORITI  ")
print("--==========================--")

while True:
    time.sleep(1000)
