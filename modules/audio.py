# Audio modules
import pyaudio
import wave
import threading
import wave
import audioop

# Timing and file modules
import os
import time

# Template matching modules
from maad import sound, util
from maad.rois import template_matching

flims = (6000, 18000)
nperseg = 1024
noverlap = 0
window = 'hann'
db_range = 80

class AudioRecorder:
    def __init__(self, chunk=1024, format=pyaudio.paInt16, channels=1, rate=44100, buffer_length=5):
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.buffer_length = buffer_length  # in seconds
        self.frames = []
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                        rate=self.rate, input=True,
                        frames_per_buffer=self.chunk)
        
        self.db = 0

    def start_recording(self):
        self.is_recording = True
        t = threading.Thread(target=self._record)
        t.start()


    def _record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.db = audioop.max(data, 2)
            self.frames.append(data)

            # Trim buffer to maintain the desired length
            max_frames = int(self.rate / self.chunk * self.buffer_length)
            self.frames = self.frames[-max_frames:]

    def stop_recording(self):
        self.is_recording = False

    def save_last_n_seconds(self, filename, seconds=3):
        frames_to_save = self.frames[-int(self.rate / self.chunk * seconds):]
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames_to_save))
        wf.close()

def get_audio_length(filename):
    with wave.open(filename, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
        return duration
    
def playFile(filename):
    chunk = 1024
    with wave.open(filename, 'rb') as wf:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

def get_templates():
    # Set spectrogram parameters
    maxLength = 0
    templates = []
    for filename in os.listdir('templates/'):
        if(filename.endswith('.wav')):
            template_length = get_audio_length('templates/' + filename)
            maxLength = max(maxLength, template_length)
            sampleVec, sampleFreq = sound.load('templates/' + filename)
            Sxx_template, _, _, _ = sound.spectrogram(sampleVec, sampleFreq, window, nperseg, noverlap, flims)
            templates.append(util.power2dB(Sxx_template, db_range))

    return templates, maxLength

def detect_barks(recorder, templates, maxLength, peak_th):
    target_name = f"output_{int(time.time())}.wav"
    recorder.save_last_n_seconds(target_name, seconds=3)
    s2, fs2 = sound.load(target_name)

    Sxx_audio, tn, fn, ext = sound.spectrogram(s2, fs2, window, nperseg, noverlap, flims)
    Sxx_audio = util.power2dB(Sxx_audio, db_range)

    # Compute the cross-correlation of spectrograms
    # ---------------------------------------------
    # Compute the cross-correlation of spectrograms and find peaks in the resulting signal using the `template matching` function. The template_matching functions gives temporal information on the location of the audio and frequency limits must be added.
    num_match = 0
    for template in templates:
        xcorrcoef, rois = template_matching(Sxx_audio, template, tn, ext, peak_th)
        if(not rois.empty):
            num_match += 1

    os.remove(target_name)

    return num_match

def recordFile():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 1
    WAVE_OUTPUT_FILENAME = f"templates/output_{int(time.time())}.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()