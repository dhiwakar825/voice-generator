import subprocess
import wave
from pathlib import Path
import os
class PiperTTS:
    VOICES = {
        'Female (US)': {
            'model': 'en_US-lessac-medium.onnx',
            'config': 'en_US-lessac-medium.onnx.json'
        },
        'Male (US)': {
            'model': 'en_US-ryan-medium.onnx',
            'config': 'en_US-ryan-medium.onnx.json'
        },
        'Female (UK)': {
            'model': 'en_GB-alba-medium.onnx',
            'config': 'en_GB-alba-medium.onnx.json'
        }
    }
    
    def __init__(self, voice='Female (US)'):
        self.model_dir = Path("models/piper")
        self.output_dir = Path("output/audio")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.set_voice(voice)
    
    def set_voice(self, voice_name):
        if voice_name not in self.VOICES:
            raise ValueError(f"Voice '{voice_name}' not found. Options: {list(self.VOICES.keys())}")
        
        self.current_voice = voice_name
        voice = self.VOICES[voice_name]
        self.model_path = self.model_dir / voice['model']
        self.config_path = self.model_dir / voice['config']
        
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
    
    def synthesize(self, text, output_filename=None):
        if output_filename is None:
            import hashlib
            hash_id = hashlib.md5(text.encode()).hexdigest()[:8]
            voice_prefix = self.current_voice.split(' ')[0].lower()
            output_filename = f"speech_{voice_prefix}_{hash_id}.wav"
        
        output_path = self.output_dir / output_filename
        
        cmd = [
            os.path.expanduser('~/bin/piper'),
            '--model', str(self.model_path),
            '--config', str(self.config_path),
            '--output_file', str(output_path)
        ]
        
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=text)
        
        if process.returncode != 0:
            raise RuntimeError(f"TTS failed: {stderr}")
        
        with wave.open(str(output_path), 'r') as wf:
            duration = wf.getnframes() / wf.getframerate()
        
        return {
            'path': str(output_path),
            'filename': output_filename,
            'duration': duration,
            'size_kb': output_path.stat().st_size / 1024,
            'voice': self.current_voice
        }

if __name__ == "__main__":
    tts = PiperTTS('Female (US)')
    result = tts.synthesize("Hello, I am a female voice.")
    print(f"Generated: {result['filename']} ({result['duration']:.1f}s)")
    
    tts.set_voice('Male (US)')
    result = tts.synthesize("Hello, I am a male voice.")
    print(f"Generated: {result['filename']} ({result['duration']:.1f}s)")