import numpy as np
from joblib import load

Model_PATH = "Saved Models/SVM.pkl"

def predict_labels(model_path, signal_data):
    svm_model = load(model_path)
    # Assuming 'signal' is your new raw signal data

    # Apply bandpass filter
    filtered_signal = bandpass_filter(signal, lowcut, highcut, fs)

    # Correct baseline drift
    corrected_signal = DC_removal(filtered_signal)

    # Extract wavelet features
    wavelet_features = extract_wavelet_features(corrected_signal)

    # Calculate PSD features
    _, psd_features = calculate_PSD(corrected_signal, fs, scaling='density')

    # Combine wavelet and PSD features if needed
    combined_features = np.concatenate((wavelet_features, psd_features))

    # Now you can send 'scaled_features' or 'combined_features' to your model for prediction

    predicted_labels = svm_model.predict(combined_features)
    labels_list = predicted_labels.tolist()

    return labels_list

# Example usage:
# Load your signal data into 'your_signal_data' as a 2D NumPy array
# model_path = 'your_model_filename.pkl'
# labels = predict_labels(model_path, your_signal_data)

# Now you can pass 'labels' to another function as needed

"""
for i in range(3):
    # Create a new figure for each sample
    plt.figure(figsize=(12, 6))

    # Plot preprocessed horizontal signal
    plt.subplot(2, 1, 1)
    plt.plot(X_horizontal_pro[i], label='Preprocessed Horizontal Signal')
    plt.title('Preprocessed Horizontal Signal - Sample {}'.format(i + 1))
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()

    # Plot PSD
    plt.subplot(2, 1, 2)
    f = X_horizontal_PSD[:, 0]
    S = X_horizontal_PSD[:,1]
    plt.semilogy(f[i], S[i])
    plt.xlim(0, 500)
    plt.ylim([1e-6, 1e3])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('Power Frequency [dB/Hz]')


    plt.tight_layout()
    plt.show()
"""

#plt.show()