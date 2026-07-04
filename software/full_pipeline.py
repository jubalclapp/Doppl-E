# Doppl-E | Full DSP Pipeline
# Captures audio from UGREEN ADC, runs FFT, identifies Doppler peak
# converts to velocity
# Author:
import sounddevice as sd
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# - Parameters -
duration = 5         # recording duration (seconds)
sample_rate = 44100  # sample rate (Hz)
device = 2           # UGREEN USB Audio Device
lambda_ = 0.0285     # HB100 wavelength (m)

# - Audio Capture -
print("Starting capture:")
audio = sd.rec(int(duration * sample_rate),
                samplerate = sample_rate, 
                channels = 1,
                device = device)
sd.wait()
audio = audio.flatten()
print("Capture complete")

# - FFT Pipeline -

# Apply Hann window
window = np.hanning(len(audio))
signal_windowed = audio * window

# Run FFT on capture
fft_result = np.fft.fft(signal_windowed)
fft_magnitude = np.abs(fft_result)

# Frequency axis
frequencies = np.fft.fftfreq(len(audio), 1/sample_rate)

# Only plot the positive frequencies to 3000Hz
positive_mask = (frequencies >= 0) & (frequencies <= 3000)

plt.figure()
plt.plot(frequencies[positive_mask], fft_magnitude[positive_mask])
plt.xlabel('Frequency(Hz)')
plt.ylabel('Magnitude')
plt.title('FFT of capture')
plt.show()

# Find the peak frequency
peaks, _ = find_peaks(fft_magnitude[positive_mask], height=10)
peak_frequencies = frequencies[positive_mask][peaks]

# Calculate velocity from peak frequency assuming HB100 hardware
velocity = (peak_frequencies * lambda_)/2    # v=f_d * lambda/2

# Print frequency and velocity data
for f, v in zip(peak_frequencies, velocity):
    print(f"Detected frequency: {f:.1f} Hz")
    print(f"Estimated velocity: {v:.2f} m/s, {v * 2.237:.2f} mph")
