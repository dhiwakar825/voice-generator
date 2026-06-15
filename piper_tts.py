"""
TTS Engine using gTTS
"""
from gtts import gTTS
from pathlib import Path
import hashlib

class PiperTTS:
    VOICES = {
        'Female (US)': {'lang': 'en', 'tld': 'com'},
        'Male (US)': {'lang': 'en', 'tld': 'co.in'},
        'Female (UK)': {'lang': 'en', 'tld': 'co.uk'},
    }
    
    def __init__(self, voice='Female (US)'):
        self.output_dir = Path("output/audio")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.set_voice(voice)
    
    def set_voice(self, voice_name):
        if voice_name not in self.VOICES:
            raise ValueError(f"Voice '{voice_name}' not found. Options: {list(self.VOICES.keys())}")
        self.current_voice = voice_name
    
    def synthesize(self, text, output_filename=None):
        if output_filename is None:
            hash_id = hashlib.md5(text.encode()).hexdigest()[:8]
            voice_prefix = self.current_voice.split(' ')[0].lower()
            output_filename = f"speech_{voice_prefix}_{hash_id}.mp3"
        
        output_path = self.output_dir / output_filename
        
        voice_config = self.VOICES[self.current_voice]
        
        tts = gTTS(text=text, lang=voice_config['lang'], tld=voice_config['tld'], slow=False)
        tts.save(str(output_path))
        
        duration = len(text.split()) * 0.4
        
        return {
            'path': str(output_path),
            'filename': output_filename,
            'duration': duration,
            'size_kb': output_path.stat().st_size / 1024,
            'voice': self.current_voice
        }