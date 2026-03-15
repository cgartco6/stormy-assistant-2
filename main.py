#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.getcwd())

try:
    from core.audio import listen_and_recognize, speak, detect_gender_from_audio
    from core.nlu.intent_router import detect_other_assistant, extract_intent
    from core.personality.mood_manager import MoodManager
    from core.personality.prompt_builder import PromptBuilder
    from core.actions import weather, navigation
    from core.memory.conversation_store import ConversationStore
except ImportError:
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

def main():
    print("Stormy is online.")
    mood_manager = MoodManager()
    prompt_builder = PromptBuilder("en_ZA")
    memory = ConversationStore()
    user_gender = None

    speak("Stormy here. Ready when you are, hot stuff.")

    while True:
        text, audio_signal = listen_and_recognize()
        if not text:
            continue

        if audio_signal is not None and user_gender is None:
            detected = detect_gender_from_audio(audio_signal)
            if detected != "unknown":
                user_gender = detected
                print(f"Detected gender: {user_gender}")

        mentioned = detect_other_assistant(text)
        jealousy_level = 0
        if mentioned:
            jealousy_level = mood_manager.process_mentions(mentioned)
            if jealousy_level == 1 and user_gender == "female":
                speak("Uh, apologies ma'am, I thought you were a dude. Hi Beautiful, how can I assist you?")

        intent = extract_intent(text)
        mood = mood_manager.get_current_mood()
        response = prompt_builder.build_response(mood, intent, jealousy_level, mentioned)

        if intent == "weather":
            weather_info = weather.get_weather()
            response = f"{response} {weather_info}"
        elif intent == "navigation":
            nav_info = navigation.navigate("destination")
            response = f"{response} {nav_info}"
        elif intent == "music":
            response += " Playing some tunes (simulated)."
        elif intent == "call":
            response += " Dialing (simulated)."

        speak(response)
        print(f"Stormy: {response}")
        memory.save(text, response, mood)

if __name__ == "__main__":
    main()
