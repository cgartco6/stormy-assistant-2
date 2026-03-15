class UserPreferences:
    def __init__(self, db_path="data/user_prefs.db"):
        self.db_path = db_path

    def get(self, key, default=None):
        return default

    def set(self, key, value):
        pass
