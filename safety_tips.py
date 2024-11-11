import random

class SafetyTipsGenerator:
    def __init__(self):
        self.tips = [
            "Always buckle up - it's your first line of defense! 🔐",
            "Keep your eyes on the road, phone in your pocket 📱",
            "Rain or snow? Take it slow! 🌧️",
            "Maintain a 3-second following distance ⏱️",
            "Check your mirrors every 5-8 seconds 👀",
            "Never drive drowsy - take breaks on long trips 😴",
            "Music's fun, but keep it at a moderate volume 🎵",
            "Plan your route before starting your journey 🗺️",
            "Regular car maintenance saves lives 🔧",
            "Be extra cautious at intersections 🚦"
        ]
    
    def get_random_tip(self):
        return random.choice(self.tips)