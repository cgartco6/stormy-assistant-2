import random
from .jealousy_tracker import JealousyTracker

class MoodManager:
    def __init__(self):
        self.base_mood = "normal"
        self.mood_probabilities = {
            "normal": 0.4,
            "playful": 0.2,
            "flirty": 0.15,
            "mean": 0.1,
            "frustrated": 0.1,
            "furious": 0.05
        }
        self.jealousy = JealousyTracker()
        self.temporary_mood = None

    def get_current_mood(self):
        if self.temporary_mood:
            return self.temporary_mood
        moods = list(self.mood_probabilities.keys())
        probs = list(self.mood_probabilities.values())
        return random.choices(moods, weights=probs)[0]

    def process_mentions(self, mentioned_assistant):
        jealousy_level = self.jealousy.update(mentioned_assistant)
        if jealousy_level == 1:
            self.temporary_mood = "annoyed"
        elif jealousy_level == 2:
            self.temporary_mood = "jealous"
        elif jealousy_level == 3:
            self.temporary_mood = "furious"
        else:
            self.temporary_mood = None
        return jealousy_level

    def reset_jealousy(self):
        self.jealousy.reset()
        self.temporary_mood = None
