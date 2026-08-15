## Doppl-E Lab | Radar Control Interface
# Real-time Doppler velocity measurement and visualization
# Verified on hardware: vehicle detection up to 20mph
# Author: Jubal Clapp

import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sounddevice as sd
from scipy.signal import butter, filtfilt
from collections import deque
import threading
import time
import zipfile
import csv
import os
from datetime import datetime

# - Audio Parameters -
sample_rate = 44100     # Hz
chunk_size = 4096       # samples/chunk      (~0.09 seconds)
window_size = 22050     # samples/FFT window (~0.5 seconds)
device = 2             # UGREEN USB Audio  Device
lambda_ = 0.0285        # HB100 signal wavelength (m)
min_freq = 80           # HPF cutoff (Hz)
max_freq = 2340         # LPF cutoff (Hz)
peak_threshold = 0.5   # minimum FFT magnitude to report a detection

# - Shared buffer - #
audio_buffer = deque(maxlen=window_size)
buffer_lock = threading.Lock()

# - Colour Scheme -
BG_DARK = "#0a0a0a"         # main background
BG_PANEL = "#141414"        # panel background
BG_CARD = "#1e1e1e"         # card/widget background
ACCENT = "#00ff88"          # green accent (radar theme)
ACCENT_RED = "#ff4444"      # red colour for stop button
TEXT_PRIMARY = "#ffffff"     # primary text
TEXT_SECONDARY = "#888888"  # secondary text
TEXT_DIM = "#444444"        # dim text

# --- Main Application ---
class DopplELab:
    def __init__(self, root):
        self.root = root
        self.root.title("Doppl-E Lab")
        self.root.geometry("1200x700")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)
        self.root.state("zoomed")
        self.root.bind('<F11>', lambda e: self.root.state(
            'normal' if self.root.state() == 'zoomed' else 'zoomed'))

        self.is_capturing = False
        self.session_start = None
        self.session_velocities = []
        self.build_ui()

    # - High-Pass Filter - #
    def apply_hpf(self, audio):
        b, a = butter(4, min_freq / (sample_rate / 2), btype='high')
        return filtfilt(b, a, audio)

    # -FFT and velocity extraction- #
    def process_buffer(self):
        with buffer_lock:
            if len(audio_buffer) < window_size:
                return None  # not enough data to make an estimate
            samples = np.array(audio_buffer)

        # Hann window
        window = np.hanning(len(samples))
        windowed = self.apply_hpf(samples) * window

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
            return None  # below detection threshold

        # Convert frequency to velocity
        velocity_ms = (peak_freq * lambda_) / 2
        velocity_mph = velocity_ms * 2.237

        return peak_freq, velocity_ms, velocity_mph, peak_magnitude, masked_freqs, masked_fft

    def audio_callback(self, indata, frames, time_info, status):
        with buffer_lock:
            audio_buffer.extend(indata[:, 0])

    def start_stream(self):
        self.stream = sd.InputStream(
            samplerate = sample_rate,
            channels = 1,
            device = device,
            blocksize = chunk_size,
            callback = self.audio_callback
        )
        self.stream.start()

    def stop_stream(self):
        if hasattr(self, "stream"):
            self.stream.stop()
            self.stream.close()

    def update_display(self):
        if not self.is_capturing:
            return

        result = self.process_buffer()

        if result:
            freq, v_ms, v_mph, mag, masked_freqs, masked_fft = result

            self.session_velocities.append(v_ms)

            # Update display
            self.vel_ms.config(text=f"{v_ms:.2f}")
            self.vel_mph.config(text=f"{v_mph:.1f} mph")
            self.vel_hz.config(text=f"{freq:.1f} Hz")

            # Update session stats
            elapsed = int(time.time() - self.session_start)
            mins = elapsed // 60
            secs = elapsed % 60
            self.stat_time.config(text=f"{mins:02d}:{secs:02d}")

            if self.session_velocities:
                self.stat_max.config(text=f"{max(self.session_velocities):.2f} m/s")
                self.stat_min.config(text=f"{min(self.session_velocities):.2f} m/s")
                avg = sum(self.session_velocities) / len(self.session_velocities)
                self.stat_avg.config(text=f"{avg:.2f} m/s")

            # Update FFT plot
            self.line.set_data(masked_freqs, masked_fft)
            self.ax.set_ylim(0, max(masked_fft) * 1.2)
            self.canvas.draw()

        else:
            # No target detected
            self.vel_ms.config(text="0.00")
            self.vel_mph.config(text="0.0 mph")
            self.vel_hz.config(text="0 Hz")

        # Update in 500ms
        self.root.after(500, self.update_display)


    def build_ui(self):
        # - Top bar -
        top_bar = tk.Frame(self.root, bg=BG_PANEL, height=60)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)

        title = tk.Label(top_bar, text="DOPPL-E LAB",
                         font=("TkDefaultFont", 18, "bold"),
                         fg=ACCENT, bg=BG_PANEL)
        title.pack(side=tk.LEFT, padx=20, pady=15)

        subtitle = tk.Label(top_bar, text="CW Doppler Radar System",
                            font=("TkDefaultFont", 18, "bold"),
                            fg=ACCENT, bg=BG_PANEL)
        subtitle.pack(side=tk.LEFT, padx=0, pady=20)

        # Info button on top right
        info_btn = tk.Button(top_bar, text="  ?  ",
                             font=("TkDefaultFont", 12, "bold"),
                             fg=TEXT_SECONDARY, bg=BG_CARD,
                             relief=tk.FLAT, cursor="hand2",
                             command=self.show_info)
        info_btn.pack(side=tk.RIGHT, padx=20, pady=12)

        # --- Main content ---
        content = tk.Frame(self.root, bg=BG_DARK)
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # --- Left panel (velocity + control) ---
        left_panel = tk.Frame(content, bg=BG_PANEL, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_panel.pack_propagate(False)

        # - Velocity display -
        vel_label = tk.Label(left_panel, text="VELOCITY",
                             font=("TkDefaultFont", 10),
                             fg=TEXT_SECONDARY, bg=BG_PANEL)
        vel_label.pack(pady=(30, 0))

        self.vel_ms = tk.Label(left_panel, text="0.00",
                               font=("TkDefaultFont", 52, "bold"),
                               fg=ACCENT, bg=BG_PANEL)
        self.vel_ms.pack()

        ms_label = tk.Label(left_panel, text="m/s",
                            font=("TkDefaultFont", 14),
                            fg=TEXT_SECONDARY, bg=BG_PANEL)
        ms_label.pack()

        self.vel_mph = tk.Label(left_panel, text="0.0 mph",
                                font=("TkDefaultFont", 18),
                                fg=TEXT_PRIMARY, bg=BG_PANEL)
        self.vel_mph.pack(pady=(5,0))

        self.vel_hz = tk.Label(left_panel, text="0 Hz",
                               font=("TkDefaultFont", 12),
                               fg=TEXT_DIM, bg=BG_PANEL)
        self.vel_hz.pack(pady=(2,20))

        # Divider
        div = tk.Frame(left_panel, bg=BG_CARD, height=1)
        div.pack(fill=tk.X, padx=20, pady=10)

        # Session stats
        stats_label = tk.Label(left_panel, text="SESSION",
                               font=("TkDefaultFont", 10),
                               fg=TEXT_SECONDARY, bg=BG_PANEL)
        stats_label.pack(pady=(10, 5))

        self.stat_time = self._stat_row(left_panel, "Duration", "00:00")
        self.stat_max = self._stat_row(left_panel, "Max", "0.00 m/s")
        self.stat_min = self._stat_row(left_panel, "Min", "0.00 m/s")
        self.stat_avg = self._stat_row(left_panel, "Avg", "0.00 m/s")

        # Divider
        div2 = tk.Frame(left_panel, bg=BG_CARD, height=1)
        div2.pack(fill=tk.X, padx=20, pady=20)

        # Start/Stop button
        self.capture_btn = tk.Button(left_panel,
                                     text="START CAPTURE",
                                     font=("TkDefaultFont", 13, "bold"),
                                     fg=BG_DARK, bg=ACCENT,
                                     relief=tk.FLAT,
                                     cursor="hand2",
                                     padx=20, pady=12,
                                     command=self.toggle_capture)
        self.capture_btn.pack(padx=20, fill=tk.X)

        # Save report button (hidden until capture complete)
        self.save_btn = tk.Button(left_panel,
                                  text="SAVE REPORT",
                                  font=("TkDefaultFont", 11),
                                  fg=TEXT_PRIMARY, bg=BG_CARD,
                                  relief=tk.FLAT,
                                  cursor="hand2",
                                  padx=20, pady=10,
                                  command=self.save_report)
        # Not packed until capture stops

        # --- Right Panel (FFT plot) ---
        right_panel = tk.Frame(content, bg=BG_PANEL)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        plot_label = tk.Label(right_panel, text="FFT SPECTRUM",
                              font=("TkDefaultFont", 10),
                              fg=TEXT_SECONDARY, bg=BG_PANEL)
        plot_label.pack(pady=(15, 5))

        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(7, 4.5))
        self.fig.patch.set_facecolor(BG_PANEL)
        self.ax.set_facecolor(BG_PANEL)
        self.ax.set_xlabel("Frequency (Hz)", color=TEXT_SECONDARY,
                           fontsize=9)
        self.ax.set_ylabel("Magnitude", color=TEXT_SECONDARY,
                           fontsize=9)
        self.ax.tick_params(colors=TEXT_SECONDARY)
        self.ax.spines[:].set_color(BG_CARD)
        self.ax.set_xlim(0, 2340)
        self.ax.set_ylim(0, 10)
        self.line, = self.ax.plot([], [], color=ACCENT, linewidth=1.5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True,
                                         padx=15, pady=(0, 15))

        # Status bar
        self.status = tk.Label(right_panel,
                               text="IDLE - Press Start Capture to begin",
                               font=("TkDefaultFont", 9),
                               fg=TEXT_DIM, bg=BG_PANEL)
        self.status.pack(pady=(0, 10))

    def _stat_row(self, parent, label, value):
        frame = tk.Frame(parent, bg=BG_PANEL)
        frame.pack(fill=tk.X, padx=20, pady=2)
        tk.Label(frame, text=label, font=("TkDefaultFont", 9),
                 fg=TEXT_SECONDARY, bg=BG_PANEL).pack(side=tk.LEFT)
        val = tk.Label(frame, text=value, font=("TkDefaultFont", 9, "bold"),
                       fg=TEXT_PRIMARY, bg=BG_PANEL)
        val.pack(side=tk.RIGHT)
        return val

    def toggle_capture(self):
        if not self.is_capturing:
            self.start_capture()
        else:
            self.stop_capture()

    def start_capture(self):
        self.is_capturing = True
        self.session_start = time.time()
        self.session_velocities = []
        self.capture_btn.config(text="STOP CAPTURE", bg=ACCENT_RED,
                                fg=TEXT_PRIMARY)
        self.save_btn.pack_forget()
        self.status.config(text="CAPTURING - Point antenna at target",
                           fg=ACCENT)
        self.start_stream()
        self.update_display()

    def stop_capture(self):
        self.is_capturing = False
        self.capture_btn.config(text="START CAPTURE", bg=ACCENT,
                                fg=BG_DARK)
        self.save_btn.pack(padx=20, fill=tk.X, pady=(10, 0))
        self.status.config(text="STOPPED - Save report or start new capture",
                           fg=ACCENT_RED)
        self.stop_stream()

    def save_report(self):
        if not self.session_velocities:
            self.status.config(text="No data to save, run a capture first",
                               fg=ACCENT_RED)
            return

        # Generate timestamp for file names
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_filename = f"dopple_session_{timestamp}.zip"

        # Ask user desired save path
        save_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip")],
            initialfile=zip_filename,
            title="Save Doppl-E Session Report"
        )

        if not save_path:
            return # user cancelled file save

        # --- Build report ---
        session_duration = int(time.time() - self.session_start)
        mins = session_duration // 60
        secs = session_duration % 60
        avg_velocity = sum(self.session_velocities) / len(self.session_velocities)

        # 1. Session summary text file
        summary = f"""DOPPL-E LAB - SESSION REPORT
        Generated :           {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        Session Duration:     {mins:02d}:{secs:02d}
        Total Detections:     {len(self.session_velocities)}
        Max Velocity:         {max(self.session_velocities):.2f} m/s ({max(self.session_velocities)*2.237:.1f} mph)
        Min Velocity:         {min(self.session_velocities):.2f} m/s ({min(self.session_velocities)*2.237:.1f} mph)
        Avg Velocity:         {avg_velocity:.2f} m/s ({avg_velocity*2.237:.1f} mph)
        {'=0*40'}
        System Configuration
        HPF Cutoff:           {min_freq} Hz
        LPF Cutoff:           {max_freq} Hz
        Min Detectable Speed: 1.14 m/s
        Sample Rate:          {sample_rate} Hz
"""

        # 2. Velocity log CSV
        csv_rows = []
        for i, v in enumerate(self.session_velocities):
            csv_rows.append([i * 0.5, round(v, 3), round(v * 2.237, 3)])

        # 3. FFT Snapshot
        fft_image_path = f"fft_snapshot_{timestamp}.png"
        self.fig.savefig(fft_image_path, facecolor=BG_PANEL,
                     bbox_inches='tight', dpi=150)

        # - Write zip file -
        with zipfile.ZipFile(save_path,  'w') as zf:
            # Summary
            zf.writestr(f"session_summary_{timestamp}.txt", summary)

            # CSV
            import io
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(["Time (s)", "Velocity (m/s)", "Velocity (mph)"])
            writer.writerows(csv_rows)
            zf.writestr(f"velocity_log_{timestamp}.csv", csv_buffer.getvalue())

            # FFT image
            zf.write(fft_image_path, f"fft_snapshot_{timestamp}.png")

        # Clean FFT image
        os.remove(fft_image_path)

        self.status.config(text=f"Report saved: {os.path.basename(save_path)}", fg=ACCENT)

    def show_info(self):
        # Placeholder for dialog
        print("Info triggered")

# -- Launch ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DopplELab(root)
    root.mainloop()