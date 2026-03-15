import pyttsx3
import threading

engine = None

def get_engine():
    global engine
    if engine is None:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'zira' in voice.id.lower() or 'female' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 0.9)
    return engine

def speak(text):
    def _speak():
        eng = get_engine()
        eng.say(text)
        eng.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()
