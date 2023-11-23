# Introduction
Welcome to Lunar Tools, a comprehensive toolkit designed to fascilitate the programming of interactive exhibitions. Our suite of simple, modular tools is crafted to offer a seamless and hopefully bug-free experience for both exhibitors and visitors.

# Installation
pip install git+https://github.com/lunarring/lunar_tools

# Audio
## AudioRecorder
```python
import lunar_tools as lt
import time
audio_recorder = lt.AudioRecorder()
audio_recorder.start_recording("myvoice.mp3")
time.sleep(3)
audio_recorder.stop_recording()    
```

## Speech2Text
```python
import lunar_tools as lt
import time
speech_detector = lt.Speech2Text()
speech_detector.start_recording()
time.sleep(3)
translation = speech_detector.stop_recording()
print(f"translation: {translation}")
```

## Text2Speech
```python
import lunar_tools as lt
text2speech = lt.Text2Speech()
text2speech = Text2Speech()
text2speech.change_voice("nova")
text2speech.generate_speech("hey there can you hear me?", "hervoice.mp3")
```

## Play sounds
```python
import lunar_tools as lt
player = lt.SoundPlayer()
player.play_sound("myvoice.mp3")
```
The playback is threaded and does not block the main application. You can stop the playback via: 
```python
player.stop_sound()
```

# Logging and terminal printing
```python
import lunar_tools as lt
logger = lt.LogPrint()  # No filename provided, will use default current_dir/logs/%y%m%d_%H%M
logger.print("white")
logger.print("red", "red")
logger.print("green", "green")
```    

# Image gen
## Generate Images with Dall-e-3
```python
import lunar_tools as lt
dalle3 = lt.Dalle3ImageGenerator()
image, revised_prompt = dalle3.generate("a beautiful red house with snow on the roof, a chimney with smoke")
```

# Devinfos
## Testing
pip install pytest

make sure you are in base folder
```python
pytest lunar_tools/tests/
```

## Get requirements
```python
pipreqs . --force
```



