#Doppl-E | Audio Device Diagnostic Tool
# Lists all avalable audio input/output devices and their device number
# Run this if sounddevice returns errors or software tools return nothing but low noise levels
# Author : Jubal Clapp
import sounddevice as sd
import numpy as np

print(sd.query_devices())
input("Press Enter to continue...") # use this break to ensure you've selected the correct devuce

duration = 3
sample_rate = 44100
device = 3 # device number, change if needed


print(f"Live: device {device}...")
audio = sd.rec(int(duration * sample_rate),
               samplerate=sample_rate,
               channels=1,
               device=device)
sd.wait()
print(f"Max amplitude: {np.max(np.abs(audio))}")
print(f"Mean amplitude: {np.mean(np.abs(audio))}")