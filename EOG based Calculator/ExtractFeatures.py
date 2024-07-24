import numpy as np
from sklearn.model_selection import train_test_split
from Preprocessing import preprocessing
from SingalPreprocessing import process_signals
import pywt
import scipy


def extract_wavelet_features(signal):
    signal = np.asarray(signal)  # Ensure signal is a 1D NumPy array

    coeffs = pywt.wavedec(signal, 'db4', level=4)
    features = []
    for coeff in coeffs:
        features += coeff.tolist()
    return features


# Add wavelet features to the raw features DataFrame
def compute_statistical_features(wavelet_coeffs):
    statistical_features = []
    for coeffs in wavelet_coeffs:
        mean = np.mean(coeffs)
        std_dev = np.std(coeffs)
        skewness = scipy.stats.skew(coeffs)
        kurtosis = scipy.stats.kurtosis(coeffs)
        statistical_features.extend([mean, std_dev, skewness, kurtosis])
    return statistical_features


def compute_morphological_features(wavelet_coeffs):
    morphological_features = []
    for coeffs in wavelet_coeffs:
        zero_crossings = np.sum(np.abs(np.diff(np.sign(coeffs))) > 0)
        peak_to_peak = np.max(coeffs) - np.min(coeffs)
        morphological_features.extend([zero_crossings, peak_to_peak])
    return morphological_features


# Extract PSD features
def calculate_PSD(x, sr, scaling='density'):
    f, S = scipy.signal.periodogram(x, sr, scaling=scaling)
    return f, S


def feature_extraction(data, fs=176):
    x_horizontal = data['Horizontal_Signal']
    x_vertical = data['Vertical_Signal']

    x_horizontal_wavelet_features = x_horizontal.apply(extract_wavelet_features)
    x_horizontal_wavelet_array = np.array(x_horizontal_wavelet_features.tolist())
    x_horizontal_PSD = np.array([
        calculate_PSD(signal, fs, scaling='density') for signal in x_horizontal
    ])

    x_vertical_wavelet_features = x_vertical.apply(extract_wavelet_features)
    x_vertical_wavelet_array = np.array(x_vertical_wavelet_features.tolist())
    x_vertical_PSD = np.array([
        calculate_PSD(signal, fs, scaling='density') for signal in x_vertical
    ])

    return {"wavelet": [x_horizontal_wavelet_array, x_vertical_wavelet_array],
            "PSD": [x_horizontal_PSD, x_vertical_PSD]}

# data = preprocessing("3-class")
# data['Horizontal_Signal'], data['Vertical_Signal'] = process_signals(data)
# features = feature_extraction_training(data)
# print(f"wavelet horizontal:\n{features["wavelet"][0]}\nhorizontal PSD:\n{features["PSD"][0]}")
