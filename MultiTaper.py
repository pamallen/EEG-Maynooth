from spectrum import *
from pylsl import StreamInlet, resolve_stream
import matplotlib.pyplot as plt

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

canal1 = list()
timestamp_list = list()
len_sample = 2000

plt.ion()

while True:

    sample, timestamp = inlet.pull_sample()

    if len(canal1) > len_sample:
        del canal1[0]
        del timestamp_list[0]

    canal1.append(sample[0])
    timestamp_list.append(timestamp)

    if len(canal1) > len_sample:
        [tapers, eigen] = dpss(2001, 2.5, 4)
        res = pmtm(canal1, e=tapers, v=eigen, show=False)
        res = pmtm(canal1, NW=2.5, show=False)
        res = pmtm(canal1, NW=2.5, k=4, show=True)

        plt.plot(res)
        plt.draw()
        plt.pause(0.01)
        plt.clf()
