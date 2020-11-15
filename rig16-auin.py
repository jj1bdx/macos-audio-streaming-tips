#!/usr/bin/env python3
import pyaudio
import signal
import sys
import time

argvs = sys.argv
argc = len(argvs)

if argc == 2:
  channels = int(argvs[1])
  devidx = None
elif argc == 3:
  channels = int(argvs[1])
  devidx = int(argvs[2])
else:
  print('Usage: ', argvs[0], 'channels [device-index]\n')
  quit()

channels = int(argvs[1])
sample_rate = 11025
sample_width = 2 # 16bit integer
sample_format = pyaudio.paInt16
framesize = 110 # 10msec

if sys.platform == 'darwin':
    CHANNELS = 1

def terminate():
    stream.stop_stream()
    stream.close()
    p.terminate()

def signal_handler(signal, frame):
    print('Terminated by CTRL/C')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def callback(in_data, frame_count, time_info, status):
    sys.stdout.buffer.write(in_data)
    return (None, pyaudio.paContinue)

p = pyaudio.PyAudio()

stream = p.open(format = sample_format,
                channels = channels,
                rate = sample_rate,
                input = True,
                input_device_index = devidx,
                frames_per_buffer = framesize,
                stream_callback = callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

terminate()
