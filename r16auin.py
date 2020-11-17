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
sample_rate = 48000
sample_width = 2 # 16bit integer
sample_format = pyaudio.paInt16

frame_size = 768 # 16msec

def terminate():
    stream.stop_stream()
    stream.close()
    p.terminate()

def signal_handler(signal, frame):
    print('Terminated by CTRL/C')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

p = pyaudio.PyAudio()

stream = p.open(format = sample_format,
                channels = channels,
                rate = sample_rate,
                input = True,
                input_device_index = devidx,
                frames_per_buffer = frame_size,
                )

# print(stream.get_input_latency(), file=sys.stderr)

while True:
    samples = stream.read(frame_size)
    sys.stdout.buffer.write(samples)

terminate()
