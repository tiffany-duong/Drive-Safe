from gtts import gTTS
import os

def create_alert_files():
    # Dictionary of alert messages
    alerts = {
        "speeding": "Warning! Speed exceeds limit. Please slow down.",
        "sharp_turn": "Caution! Sharp turn ahead. Reduce speed.",
        "phone_use": "Alert! Phone use detected. Keep eyes on road.",
        "sudden_brake": "Notice! Sudden braking detected. Maintain safe distance.",
        "lane_departure": "Warning! Lane departure detected. Stay in lane."
    }
    
    # Create alerts directory if it doesn't exist
    if not os.path.exists("alerts"):
        os.makedirs("alerts")
    
    # Generate audio files
    for filename, text in alerts.items():
        print(f"Creating alert for: {filename}")
        tts = gTTS(text=text, lang='en')
        tts.save(f"alerts/{filename}.mp3")
        print(f"Created: alerts/{filename}.mp3")

if __name__ == "__main__":
    print("Starting to create alert files...")
    create_alert_files()
    print("Finished creating all alert files!") 