#!/usr/bin/env python3
import speech_recognition as sr

def test_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Testing microphone... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"✅ Microphone works! You said: {text}")
        except Exception as e:
            print(f"❌ Microphone error: {e}")

if __name__ == '__main__':
    test_microphone()
