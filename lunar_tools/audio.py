#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyaudio
import tempfile
import wave
from pydub import AudioSegment
import threading
import os
from openai import OpenAI
from logprint import Logger


class AudioRecorder:
    """
    A class to handle audio recording.

    Attributes:
        audio_format (pyaudio.paInt16): Format of the audio recording.
        channels (int): Number of audio channels.
        rate (int): Sampling rate.
        chunk (int): Number of frames per buffer.
        frames (list): List to hold audio frames.
        is_recording (bool): Flag to check if recording is in progress.
        audio (pyaudio.PyAudio): PyAudio instance.
        stream (pyaudio.Stream): Audio stream.
        output_filename (str): Output file name.
    """

    def __init__(
        self,
        audio_format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        chunk=1024
    ):
        """
        Initialize the audio recorder.

        Args:
            audio_format (constant): Format of the audio recording.
            channels (int): Number of audio channels.
            rate (int): Sampling rate.
            chunk (int): Number of frames per buffer.
        """
        self.audio_format = audio_format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.frames = []
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.output_filename = None

    def _record(self):
        """
        Internal method to handle the audio recording process.
        Converts the recorded frames to MP3 format.
        """
        self.stream = self.audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        print("Recording...")
        self.frames = []

        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

        print("Finished recording.")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        # Convert to MP3
        raw_data = b''.join(self.frames)
        wav_audio = AudioSegment(
            data=raw_data,
            sample_width=self.audio.get_sample_size(self.audio_format),
            frame_rate=self.rate,
            channels=self.channels
        )
        wav_audio.export(self.output_filename, format="mp3")

    def start_recording(self, output_filename=None):
        """
        Start the audio recording.

        Args:
            output_filename (str): The filename for the output file. If None, a temporary file is created.
        """
        if not self.is_recording:
            self.is_recording = True
            if output_filename is None:
                temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                self.output_filename = temp_file.name
                temp_file.close()
            else:
                if not output_filename.endswith('.mp3'):
                    raise ValueError("Output filename must have a .mp3 extension")
                self.output_filename = output_filename
            self.thread = threading.Thread(target=self._record)
            self.thread.start()

    def stop_recording(self):
        """
        Stop the audio recording and join the recording thread.
        """
        if self.is_recording:
            self.is_recording = False
            self.thread.join()


class SpeechDetector:
    def __init__(self, client=None, logger=None, init_audiorecorder=False):
        if client is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("No OPENAI_API_KEY found in environment variables")
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = client
        self.logger = logger if logger else Logger()
        if init_audiorecorder:
            self.audio_recorder = AudioRecorder()
        else:
            self.audio_recorder = None

    def start_recording(self):
        if self.audio_recorder is None:
            raise ValueError("Audio recorder is not available")
        self.audio_recorder.start_recording()

    def stop_recording(self):
        if self.audio_recorder is None:
            raise ValueError("Audio recorder is not available")
        self.audio_recorder.stop_recording()
        return self.translate(self.audio_recorder.output_filename)

    def translate(self, audio_filepath):
        if not os.path.exists(audio_filepath):
            raise FileNotFoundError(f"Audio file not found: {audio_filepath}")
        with open(audio_filepath, "rb") as audio_file:
            transcript = self.client.audio.translations.create(
                model="whisper-1", 
                file=audio_file
            )
        return transcript.text

    

#%% EXAMPLE USE        
if __name__ == "__main__":
    
    import time
    speech_detector = SpeechDetector(init_audiorecorder=True)
    speech_detector.start_recording()
    time.sleep(3)
    speech_detector.stop_recording()
    
    