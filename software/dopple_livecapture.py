# Doppl-E | Real-Time Streaming Pipeline | Stage 4: Real-time streaming pipeline
# Continuously captures audio, runs FFT, and outputs a live velocity estimate in the terminal
# Verified on hardware 8/2/26: hand movement and vehicle detection(at 3-7mph)
# Author: Jubal Clapp

import numpy as np
import sounddevice as sd
from scipy.signal import butter, filtfilt
from collections import deque
import threading

# -Set Parameters- #
sample_rate = 44100     # Hz
chunk_size = 4096       # samples/chunk      (~0.09 seconds)
window_size = 22050     # samples/FFT window (~0.5 seconds)
device = 1              # USB Audio  Device
lambda_ = 0.0285        # HB100 signal wavelength (m)
min_freq = 80           # HPF cutoff (Hz)
max_freq = 2340         # LPF cutoff (Hz)
peak_threshold = 0.5    # minimum FFT magnitude to report a detection

# -Shared buffer- #
audio_buffer = deque(maxlen=window_size)
buffer_lock = threading.Lock()

# -High-Pass Filter- #
def apply_hpf(audio):
    b, a = butter(4, min_freq / (sample_rate / 2), btype='high')
    return filtfilt(b, a, audio)

# -FFT and velocity extraction- #
def process_buffer():
    with buffer_lock:
        if len(audio_buffer) < window_size:
            return None   # not enough data to make an estimate
        samples = np.array(audio_buffer)

    # Hann window
    window = np.hanning(len(samples))
    windowed = apply_hpf(samples) * window

    # FFT
    fft_result = np.abs(np.fft.fft(windowed))
    frequencies = np.fft.fftfreq(len(samples), 1 / sample_rate)

    # Positive frequencies in detection range
    mask = (frequencies >= min_freq) & (frequencies <= max_freq)
    masked_freqs = frequencies[mask]
    masked_fft = fft_result[mask]

    if len(masked_fft) == 0:
        return None

    # Find detected peak
    peak_idx = np.argmax(masked_fft)
    peak_magnitude = masked_fft[peak_idx]
    peak_freq = masked_freqs[peak_idx]

    if peak_magnitude < peak_threshold:
        return None # below detection threshold

    # Convert frequency to velocity
    velocity_ms = (peak_freq * lambda_) / 2
    velocity_mph = velocity_ms * 2.237

    return peak_freq, velocity_ms, velocity_mph, peak_magnitude

# -Audio callback- #
def audio_callback(indata, frames, time, status):
    with buffer_lock:
        audio_buffer.extend(indata[:, 0])

# -Central Streaming Loop- #
def main():
    print("Doppl-E Real-Time Streaming Pipeline")
    print(f"Device: {device} | Sample Rate: {sample_rate}Hz")
    print(f"Detection range: {min_freq}-{max_freq} Hz")
    print("Stream starting: press Ctrl+C to stop\n")

    with sd.InputStream(samplerate=sample_rate,
                        channels = 1,
                        device = device,
                        blocksize = chunk_size,
                        callback = audio_callback):
        while True:
            result = process_buffer()
            if result:
                freq, v_ms, v_mph, mag = result
                print(f"Detected: {freq:.1f} Hz |"
                      f"{v_ms:.2f} m/s | "
                      f"{v_mph:.1f} mph| "
                      f"magnitude: {mag:.2f}")
            else:
                print("No target detected: check connection and aperture orientation")

            sd.sleep(500) # only update in 0.5 second intervals

if __name__ == "__main__":
    main()


