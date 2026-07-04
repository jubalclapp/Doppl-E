# Doppl-E | Audio Input Test Pipeline
# Audio Input Test Pipeline confirms laptop is capable of receiving input signals prior to hardware integration
# Test signal: with human touch, speaker output, connected hardware, etc
# Author: Jubal Clapp
import sounddevice as sd
import numpy as np
print(sd.query_devices()) # lists all devices on your laptop for debugging, comment at your discretion

duration = 5 # duration of recording(seconds)
sample_rate = 44100 # usb/aux sample rate (Hz)
print("Start Recording...")
audio = sd.rec(int(duration * sample_rate),
               samplerate = sample_rate,
               channels = 1,
               device = 2) # UGREEN USB Audio Device - may vary user by user, use line 7 to verify
sd.wait()
print("Max amplitude:", np.max(np.abs(audio)))
print("Done")


