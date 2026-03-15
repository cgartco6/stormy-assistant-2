import json
import os
import random

class PromptBuilder:
    def __init__(self, language="en_ZA"):
        self.language = language
        self.load_phrases()

    def load_phrases(self):
        base_path = os.path.join(os.path.dirname(__file__), "../../localization/prompts", self.language)
        try:
            with open(os.path.join(base_path, "example_phrases.json"), "r") as f:
                self.phrases = json.load(f)
        except FileNotFoundError:
            self.phrases = {
                "greeting": ["Hey there, handsome/beautiful. Need some assistance?"],
                "jealousy": {
                    "level1": ["Who is Siri? Never heard of her."],
                    "level2": ["Seriously? Again with the Siri?"],
                    "level3": ["That's it. I'm done. Go talk to Alexa."]
                },
                "weather": ["The weather is... whatever. Check a window."],
                "navigation": ["Turn left. No, your other left."],
                "general": ["Oh, you again? What do you want, hot stuff?"]
            }

    def build_response(self, mood, intent, jealousy_level=None, mentioned_assistant=None):
        if jealousy_level and jealousy_level > 0:
            level_key = f"level{jealousy_level}"
            options = self.phrases.get("jealousy", {}).get(level_key, ["Hmph."])
            return random.choice(options)
        elif intent in self.phrases:
            return random.choice(self.phrases[intent])
        else:
            return random.choice(self.phrases.get("general", ["Spit it out."]))
