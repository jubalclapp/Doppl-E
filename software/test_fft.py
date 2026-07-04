# Doppl-E | Artificial Signal FFT Test Script
# Test DSP pipeline on an artificial signal before direct hardware integration
# Artificially generated signal is designed to be replaced by an HB100 IF signal
# Author: Jubal Clapp

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Parameters
sample_rate = 44100 # Sample rate of ADC(Hz)
duration = 1.0      # Seconds
frequency = 800     # Simulated IF signal, Hz

# Time axis
t = np.linspace(0, duration, int(sample_rate * duration))

# Raw sine signal
signal = np.sin(2 * np.pi * frequency * t)

plt.plot(t[:200], signal[:200])  # Small window selected to make it readable to the user
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title(f'Synthetic {frequency}Hz sine signal')
plt.show()

# Sine signal with added noise
noise = np.random.normal(0, 0.5, len(t))
signal_noisy = signal + noise

plt.plot(t[:200], signal_noisy[:200])  # Small window selected to make it readable to the user
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title(f'Noisy {frequency}Hz sine signal')
plt.show()

# Apply Hann window
window = np.hanning(len(signal_noisy))
signal_windowed = signal_noisy * window

# Run FFT on noisy signal
fft_result = np.fft.fft(signal_windowed)
fft_magnitude = np.abs(fft_result)

# Frequency axis
frequencies = np.fft.fftfreq(len(t), 1/sample_rate)

# Only plot the positive frequencies to 3000Hz
positive_mask = (frequencies >= 0) & (frequencies <= 3000)

plt.figure()
plt.plot(frequencies[positive_mask], fft_magnitude[positive_mask])
plt.xlabel('Frequency(Hz)')
plt.ylabel('Magnitude')
plt.title('FFT of noisy signal')
plt.axvline(x=frequency, color='r', linestyle='--', label=f'Expected {frequency} Hz')
plt.legend()
plt.show()

# Find the peak frequency
peaks, _ = find_peaks(fft_magnitude[positive_mask], height=1000)
peak_frequencies = frequencies[positive_mask][peaks]

# Calculate velocity from peak frequency assuming HB100 hardware
wavelength = 3e8 / 10.525e9  # c/f_HB100, in meters
velocity = (peak_frequencies * wavelength)/2    # v=f_d * lambda/2

# Print frequency and velocity data
for f, v in zip(peak_frequencies, velocity):
    print(f"Detected frequency: {f:.1f} Hz")
    print(f"Estimated velocity: {v:.2f} m/s, {v * 2.237:.2f} mph")
