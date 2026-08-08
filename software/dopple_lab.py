## Doppl-E Lab |


import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.is_capturing = False
        self.build_ui()

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
        self.capture_btn.config(text="STOP CAPTURE", bg=ACCENT_RED,
                                fg=TEXT_PRIMARY)
        self.save_btn.pack_forget()
        self.status.config(text="CAPTURING - Point antenna at target",
                           fg=ACCENT)

    def stop_capture(self):
        self.is_capturing = False
        self.capture_btn.config(text="START CAPTURE", bg=ACCENT,
                                fg=BG_DARK)
        self.save_btn.pack(padx=20, fill=tk.X, pady=(10, 0))
        self.status.config(text="STOPPED - Save report or start new capture",
                           fg=ACCENT_RED)

    def save_report(self):
        # Placeholder for report generation
        print("Save report triggered")

    def show_info(self):
        # Placeholder for dialog
        print("Info triggered")

# -- Launch ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DopplELab(root)
    root.mainloop()