import numpy as np

def detect_gender_from_audio(audio_signal, sample_rate=16000):
    if len(audio_signal) == 0:
        return "unknown"
    signal = audio_signal.astype(float)
    autocorr = np.correlate(signal, signal, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    min_period = int(sample_rate / 300)
    if len(autocorr) <= min_period:
        return "unknown"
    peak_idx = np.argmax(autocorr[min_period:]) + min_period
    if peak_idx == 0:
        return "unknown"
    pitch = sample_rate / peak_idx
    return "female" if pitch > 165 else "male"
