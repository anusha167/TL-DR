import os
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")

def generate_audio(summary, url):
    """Converts summary text to audio using gTTS (free, no API key needed)"""
    
    filename = str(abs(hash(url))) + ".mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    
    try:
        tts = gTTS(text=summary, lang='en', slow=False)
        tts.save(filepath)
        print(f"Audio saved: {filename}")
        return filename
    
    except Exception as e:
        print(f"TTS failed: {e}")
        return None