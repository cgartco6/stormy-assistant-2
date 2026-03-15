import random

def get_weather(location=None):
    conditions = ["sunny", "cloudy", "rainy", "windy", "stormy"]
    temp = random.randint(10, 35)
    cond = random.choice(conditions)
    if location:
        return f"In {location}, it's {cond} and {temp}°C."
    return f"Right now it's {cond} and {temp}°C."
