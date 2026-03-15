import re

OTHER_ASSISTANTS = ["siri", "alexa", "google", "cortana", "bixby", "hey google", "ok google"]

def detect_other_assistant(text):
    text_lower = text.lower()
    for name in OTHER_ASSISTANTS:
        if name in text_lower:
            return name
    return None

def extract_intent(text):
    text = text.lower()
    if "weather" in text:
        return "weather"
    elif "navigate" in text or "direction" in text or "route" in text:
        return "navigation"
    elif "play" in text and ("music" in text or "song" in text):
        return "music"
    elif "call" in text:
        return "call"
    else:
        return "general"
