import speech_recognition as sr
import numpy as np
import pyaudio
import wave
import tempfile
import os
import time

def listen_and_recognize(timeout=5, phrase_limit=10):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        except sr.WaitTimeoutError:
            return "", None

    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with open(temp_wav.name, "wb") as f:
        f.write(audio.get_wav_data())

    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"🗣️ You said: {text}")
    except (sr.UnknownValueError, sr.RequestError):
        text = ""

    wf = wave.open(temp_wav.name, 'rb')
    signal = np.frombuffer(wf.readframes(-1), dtype=np.int16)
    wf.close()
    time.sleep(0.1)
    os.unlink(temp_wav.name)

    return text, signal
