import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from scipy.signal import iirfilter, filtfilt


def harmonic_signal(t, amplitude, frequency, phase):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)


def generate_noise(t, noise_mean, noise_covariance):
    return np.random.normal(noise_mean, np.sqrt(noise_covariance), t.shape)


class HarmonicGUI:
    def __init__(self, master):
        self.master = master
        master.title("Harmonic with Noise and Filter")

        self.amplitude = tk.DoubleVar(value=1.0)
        self.frequency = tk.DoubleVar(value=1.0)
        self.phase = tk.DoubleVar(value=0.0)
        self.noise_mean = tk.DoubleVar(value=0.0)
        self.noise_covariance = tk.DoubleVar(value=0.1)
        self.show_noise = tk.BooleanVar(value=False)
        self.show_filtered = tk.BooleanVar(value=False)
        self.cutoff_frequency = tk.DoubleVar(value=1.0)

        self.prev_amplitude = self.amplitude.get()
        self.prev_frequency = self.frequency.get()
        self.prev_phase = self.phase.get()
        self.prev_noise_mean = self.noise_mean.get()
        self.prev_noise_covariance = self.noise_covariance.get()

        self.fig, self.ax = plt.subplots()
        self.harmonic_plot, = self.ax.plot([], [], label='Harmonic Signal', color='blue')
        self.noise_plot, = self.ax.plot([], [], label='Signal with Noise', color='red')
        self.filtered_plot, = self.ax.plot([], [], label='Filtered Signal', linestyle='--', color='green')
        self.ax.legend()
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.create_sliders()
        self.create_filter_controls()
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_parameters)
        self.reset_button.pack()

        self.t = np.linspace(0, 1, 1000)
        self.current_signal = harmonic_signal(self.t, self.amplitude.get(), self.frequency.get(), self.phase.get())
        self.current_noise = generate_noise(self.t, self.noise_mean.get(), self.noise_covariance.get())

        self.update_plot()

    def create_sliders(self):
        self.amplitude_slider = tk.Scale(self.master, label="Amplitude", from_=0.1, to=10.0, resolution=0.1,
                                         orient=tk.HORIZONTAL, variable=self.amplitude,
                                         command=self.update_plot)
        self.amplitude_slider.pack()

        self.frequency_slider = tk.Scale(self.master, label="Frequency", from_=0.1, to=10.0, resolution=0.1,
                                         orient=tk.HORIZONTAL, variable=self.frequency,
                                         command=self.update_plot)
        self.frequency_slider.pack()

        self.phase_slider = tk.Scale(self.master, label="Phase", from_=0, to=2*np.pi, resolution=0.1,
                                     orient=tk.HORIZONTAL, variable=self.phase,
                                     command=self.update_plot)
        self.phase_slider.pack()

        self.noise_mean_slider = tk.Scale(self.master, label="Noise Mean", from_=-1.0, to=1.0, resolution=0.1,
                                          orient=tk.HORIZONTAL, variable=self.noise_mean,
                                          command=self.update_plot)
        self.noise_mean_slider.pack()

        self.noise_covariance_slider = tk.Scale(self.master, label="Noise Covariance", from_=0.01, to=1.0, resolution=0.01,
                                                orient=tk.HORIZONTAL, variable=self.noise_covariance,
                                                command=self.update_plot)
        self.noise_covariance_slider.pack()

        self.show_noise_checkbox = tk.Checkbutton(self.master, text="Show Noise", variable=self.show_noise,
                                                  command=self.update_plot)
        self.show_noise_checkbox.pack()

    def create_filter_controls(self):
        self.cutoff_frequency_slider = tk.Scale(self.master, label="Cutoff Frequency", from_=0.1, to=10.0, resolution=0.1,
                                                orient=tk.HORIZONTAL, variable=self.cutoff_frequency,
                                                command=self.update_plot)
        self.cutoff_frequency_slider.pack()

        self.show_filtered_checkbox = tk.Checkbutton(self.master, text="Show Filtered Signal", variable=self.show_filtered,
                                                     command=self.update_plot)
        self.show_filtered_checkbox.pack()

    def update_plot(self, event=None):
        if self.amplitude.get() != self.prev_amplitude or self.frequency.get() != self.prev_frequency or self.phase.get() != self.prev_phase:
            self.current_signal = harmonic_signal(self.t, self.amplitude.get(), self.frequency.get(), self.phase.get())
            self.prev_amplitude = self.amplitude.get()
            self.prev_frequency = self.frequency.get()
            self.prev_phase = self.phase.get()

        if self.noise_mean.get() != self.prev_noise_mean or self.noise_covariance.get() != self.prev_noise_covariance:
            self.current_noise = generate_noise(self.t, self.noise_mean.get(), self.noise_covariance.get())
            self.prev_noise_mean = self.noise_mean.get()
            self.prev_noise_covariance = self.noise_covariance.get()

        if self.show_noise.get():
            signal_with_noise = self.current_signal + self.current_noise
        else:
            signal_with_noise = self.current_signal

        self.harmonic_plot.set_data(self.t, self.current_signal)
        self.noise_plot.set_data(self.t, signal_with_noise)

        if self.show_filtered.get():
            nyquist = 0.5 * len(self.t)
            normal_cutoff = self.cutoff_frequency.get() / nyquist
            b, a = iirfilter(4, normal_cutoff, btype='low', analog=False, ftype='butter')
            filtered_signal = filtfilt(b, a, signal_with_noise)
            self.filtered_plot.set_data(self.t, filtered_signal)
            self.filtered_plot.set_visible(True)
        else:
            self.filtered_plot.set_visible(False)

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(-10, 10)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def reset_parameters(self):
        self.amplitude.set(1.0)
        self.frequency.set(1.0)
        self.phase.set(0.0)
        self.noise_mean.set(0.0)
        self.noise_covariance.set(0.1)
        self.show_noise.set(False)
        self.show_filtered.set(False)
        self.cutoff_frequency.set(1.0)
        self.prev_amplitude = self.amplitude.get()
        self.prev_frequency = self.frequency.get()
        self.prev_phase = self.phase.get()
        self.prev_noise_mean = self.noise_mean.get()
        self.prev_noise_covariance = self.noise_covariance.get()
        self.current_signal = harmonic_signal(self.t, self.amplitude.get(), self.frequency.get(), self.phase.get())
        self.current_noise = generate_noise(self.t, self.noise_mean.get(), self.noise_covariance.get())
        self.update_plot()


root = tk.Tk()
app = HarmonicGUI(root)
root.mainloop()