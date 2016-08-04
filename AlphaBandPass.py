from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt
from scipy import arange
from scipy.signal import butter, lfilter, freqz
import numpy as np

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

canal1 = list()
timestamp_list = list()
len_sample = 2000

plt.ion()


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


while True:

    sample, timestamp = inlet.pull_sample()

    if len(canal1) > len_sample:
        del canal1[0]
        del timestamp_list[0]

    canal1.append(sample[0])
    timestamp_list.append(timestamp)

    if len(canal1) > len_sample:
        fs = 500
        lowcut = 7.5
        highcut = 12.5

        b, a = butter_bandpass(lowcut, highcut, fs)
        w, h = freqz(b, a, worN=2000)

        y = butter_bandpass_filter(canal1, lowcut, highcut, fs)

        frq = arange(len_sample) * 500 / len_sample
        y = np.delete(y, 0)

        plt.plot(frq,y)
        plt.xlim(0, max(frq) / 2)
        plt.draw()
        plt.pause(0.01)
        plt.clf()


# EEG-Maynooth
