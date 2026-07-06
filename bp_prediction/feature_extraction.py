from scipy.signal import find_peaks
import numpy as np

FS = 125
MIN_PEAK = 7
MAX_PEAK = 30

# =====================
# FEATURE EXTRACTION
# =====================

def extract_features(ppg_bandpass):

    # =====================
    # Peak Detection
    # =====================

    peaks_ppg, peaks_properties = find_peaks(
        ppg_bandpass,
        distance=int(0.4 * FS),
        prominence=0.05
    )

    valleys_ppg, _ = find_peaks(
        -ppg_bandpass,
        distance=int(0.4 * FS)
    )

    jumlah_peaks_ppg = len(peaks_ppg)

    if jumlah_peaks_ppg < MIN_PEAK or jumlah_peaks_ppg > MAX_PEAK:
        return None

    if jumlah_peaks_ppg < 2:
        return None

    # =====================
    # Heart Rate
    # =====================

    hr = jumlah_peaks_ppg * 6

    # =====================
    # Statistik Dasar
    # =====================

    mean_ppg = np.mean(ppg_bandpass)
    std_ppg = np.std(ppg_bandpass)

    min_ppg = np.min(ppg_bandpass)
    max_ppg = np.max(ppg_bandpass)

    amplitude_ppg = max_ppg - min_ppg

    auc = np.trapezoid(np.abs(ppg_bandpass))

    # =====================
    # Peak Height
    # =====================

    peaks_values = ppg_bandpass[peaks_ppg]

    mean_peak_height = np.mean(peaks_values)
    std_peak_height = np.std(peaks_values)
    max_peak_height = np.max(peaks_values)

    # =====================
    # Peak Interval
    # =====================

    intervals_ppg = np.diff(peaks_ppg) / FS

    mean_interval = np.mean(intervals_ppg)
    std_interval = np.std(intervals_ppg)

    # =====================
    # Prominence
    # =====================

    prominence_values = peaks_properties["prominences"]

    mean_prominence = np.mean(prominence_values)
    std_prominence = np.std(prominence_values)

    # =====================
    # Rise Time
    # Decay Time
    # Pulse Width
    # =====================

    rise_times = []
    decay_times = []
    pulse_widths = []

    for i in range(len(valleys_ppg) - 1):

        valley_now = valleys_ppg[i]
        valley_next = valleys_ppg[i + 1]

        peak_between = peaks_ppg[
            (peaks_ppg > valley_now) &
            (peaks_ppg < valley_next)
        ]

        if len(peak_between) == 0:
            continue

        peak = peak_between[0]

        rise_time = (peak - valley_now) / FS
        decay_time = (valley_next - peak) / FS
        pulse_width = (valley_next - valley_now) / FS

        rise_times.append(rise_time)
        decay_times.append(decay_time)
        pulse_widths.append(pulse_width)

    if len(rise_times) == 0:
        return None

    mean_rise_time = np.mean(rise_times)
    std_rise_time = np.std(rise_times)

    mean_decay_time = np.mean(decay_times)
    std_decay_time = np.std(decay_times)

    mean_pulse_width = np.mean(pulse_widths)
    std_pulse_width = np.std(pulse_widths)

    # =====================
    # Return Feature
    # =====================

    return {

        "jumlah_peaks_ppg": jumlah_peaks_ppg,

        "mean_ppg": mean_ppg,
        "std_ppg": std_ppg,

        "min_ppg": min_ppg,
        "max_ppg": max_ppg,

        "amplitude_ppg": amplitude_ppg,

        "hr": hr,

        "Mean Interval PPG": mean_interval,
        "Std Interval PPG": std_interval,

        "Mean Peak Height": mean_peak_height,
        "Std Peak Height": std_peak_height,
        "Max Peak Height": max_peak_height,

        "Mean Prominence": mean_prominence,
        "Std Prominence": std_prominence,

        "auc": auc,

        "mean_rise_time": mean_rise_time,
        "std_rise_time": std_rise_time,

        "mean_decay_time": mean_decay_time,
        "std_decay_time": std_decay_time,

        "mean_pulse_width": mean_pulse_width,
        "std_pulse_width": std_pulse_width,
    }
