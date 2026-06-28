from pathlib import Path
from hashlib import md5
from gtts import gTTS
import pygame
import time

AUDIO_FOLDER = Path("audio")
AUDIO_FOLDER.mkdir(exist_ok=True)

pygame.mixer.init()

def _generate_filename(text: str) -> Path:
  file_hash = md5(text.encode()).hexdigest()

  return AUDIO_FOLDER / f"{file_hash}.mp3"

def _generate_audio(text: str, filepath: Path):
  print("Generating audio")

  tts = gTTS(
    text=text,
    lang="id",
    slow=False
  )

  tts.save(str(filepath))

  print("Audio generated")

def _play_audio(filepath: Path):
  pygame.mixer.music.load(str(filepath))
  pygame.mixer.music.play()
  
  while pygame.mixer.music.get_busy():
    time.sleep(0.1)

def text_to_speech(text: str):
  filepath = _generate_filename(text)

  if not filepath.exists():
    _generate_audio(text, filepath)
  else:
    print("Audio telah tersedia")
  
  _play_audio(filepath)
