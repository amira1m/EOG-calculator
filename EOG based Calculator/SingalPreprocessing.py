# import matplotlib.pyplot as plt
from scipy.signal import resample
import numpy as np
from scipy.signal import butter, filtfilt, detrend
from Preprocessing import preprocessing


def bandpass_filter(signal, low_cut, high_cut, fs, order=2):
    nyquist = 0.5 * fs  # Nyquist frequency
    low = low_cut / nyquist
    high = high_cut / nyquist
    b, a = butter(order, [low, high], btype='bandpass')
    return filtfilt(b, a, signal)


def resample_signal(signal, fs):
    new_fs = 256
    resampled_signal = resample(signal, int(len(signal) * new_fs / fs))
    return resampled_signal


def DC_removal(signal):
    mean_value = np.mean(signal)
    return signal - mean_value


def normalize_signal(signal):
    min_val = min(signal)
    max_val = max(signal)

    # Perform min-max normalization
    normalized_data = [(x - min_val) / (max_val - min_val) for x in signal]
    return normalized_data


def process_signals(data):
    x_horizontal = data['Horizontal_Signal']
    x_vertical = data['Vertical_Signal']
    fs = 176
    low_cut = 0.5
    high_cut = 20
    x_horizontal = x_horizontal.apply(lambda signal: bandpass_filter(signal, low_cut, high_cut, fs))
    x_horizontal = x_horizontal.apply(DC_removal)
    x_vertical = x_vertical.apply(lambda signal: bandpass_filter(signal, low_cut, high_cut, fs))
    x_vertical = x_vertical.apply(DC_removal)

    return x_horizontal, x_vertical


# data = preprocessing("3-class")
#
# print(f"data Before:\n {data.head(5)}")
# data['Horizontal_Signal'], data['Vertical_Signal'] = process_signals(data)
# print(f"data After:\n {data.head(5)}")
