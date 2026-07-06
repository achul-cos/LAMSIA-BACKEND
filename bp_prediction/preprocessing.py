import numpy as np
from scipy.signal import butter, filtfilt, resample

def bandpass(signal, low=0.5, high=5, fs=125, order=2):
  b, a = butter(order, [low/(fs/2), high/(fs/2)], btype='band')
  return filtfilt(b, a, signal)

def preprocessing(ir):
  ir = resample(ir, 1250)

  ir = bandpass(ir)

  return ir
