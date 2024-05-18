import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from scipy.signal import iirfilter, filtfilt

# Функція створення зашумленої гармоніки
def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    t = np.linspace(0, 1, 1000)
    harmonic_signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), t.shape)
        signal_with_noise = harmonic_signal + noise
        return t, signal_with_noise, harmonic_signal
    else:
        return t, harmonic_signal, harmonic_signal


class HarmonicGUI:
    def __init__(self, master):
        self.master = master
        master.title("Harmonic with Noise and Filter")

        # Ініціалізація змінних для параметрів сигналу та фільтра
        self.amplitude = tk.DoubleVar(value=1.0)
        self.frequency = tk.DoubleVar(value=1.0)
        self.phase = tk.DoubleVar(value=0.0)
        self.noise_mean = tk.DoubleVar(value=0.0)
        self.noise_covariance = tk.DoubleVar(value=0.1)
        self.show_noise = tk.BooleanVar(value=False)
        self.show_filtered = tk.BooleanVar(value=False)
        self.cutoff_frequency = tk.DoubleVar(value=1.0)

        # Створення графіка для відображення сигналу
        self.fig, self.ax = plt.subplots()
        self.plot, = self.ax.plot([], [], label='Signal with Noise')
        self.filtered_plot, = self.ax.plot([], [], label='Filtered Signal', linestyle='--')
        self.ax.legend()
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Створення елементів управління для налаштування параметрів
        self.create_sliders()
        self.create_filter_controls()
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_parameters)
        self.reset_button.pack()

        self.update_plot()

    def create_sliders(self):
        # Створення повзунків для налаштування параметрів гармонічного сигналу та шуму
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
        # Створення повзунка та чекбоксу для налаштування параметрів фільтра
        self.cutoff_frequency_slider = tk.Scale(self.master, label="Cutoff Frequency", from_=0.1, to=10.0, resolution=0.1,
                                                orient=tk.HORIZONTAL, variable=self.cutoff_frequency,
                                                command=self.update_plot)
        self.cutoff_frequency_slider.pack()

        self.show_filtered_checkbox = tk.Checkbutton(self.master, text="Show Filtered Signal", variable=self.show_filtered,
                                                     command=self.update_plot)
        self.show_filtered_checkbox.pack()

    def update_plot(self, event=None):
        # Оновлення графіка при зміні параметрів
        t, signal_with_noise, harmonic_signal = harmonic_with_noise(self.amplitude.get(), self.frequency.get(), self.phase.get(),
                                                                    self.noise_mean.get(), self.noise_covariance.get(), self.show_noise.get())
        self.plot.set_data(t, signal_with_noise)

        if self.show_filtered.get():
            # Застосування фільтра до сигналу
            b, a = iirfilter(4, self.cutoff_frequency.get() / (0.5 * 1000), btype='low', ftype='butter')
            filtered_signal = filtfilt(b, a, signal_with_noise)
            self.filtered_plot.set_data(t, filtered_signal)
            self.filtered_plot.set_visible(True)
        else:
            self.filtered_plot.set_visible(False)

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(-10, 10)
        self.canvas.draw()

    def reset_parameters(self):
        # Скидання параметрів до значень за замовчуванням
        self.amplitude.set(1.0)
        self.frequency.set(1.0)
        self.phase.set(0.0)
        self.noise_mean.set(0.0)
        self.noise_covariance.set(0.1)
        self.show_noise.set(False)
        self.show_filtered.set(False)
        self.cutoff_frequency.set(1.0)
        self.update_plot()


root = tk.Tk()
app = HarmonicGUI(root)
root.mainloop()
