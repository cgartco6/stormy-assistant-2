class JealousyTracker:
    def __init__(self):
        self.level = 0
        self.last_mention = None
        self.count = 0

    def update(self, mentioned_assistant):
        if mentioned_assistant == self.last_mention:
            self.count += 1
        else:
            self.count = 1
            self.last_mention = mentioned_assistant
        if self.count >= 3:
            self.level = 3
        elif self.count == 2:
            self.level = 2
        elif self.count == 1:
            self.level = 1
        return self.level

    def reset(self):
        self.level = 0
        self.count = 0
        self.last_mention = None
