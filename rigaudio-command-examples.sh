# Running JTDX or WSJT-X on macOS side
# Running flrig and audio I/O on Linux (Raspberry Pi) side

# Linux command 1
# Linux real device audio input -> network
arecord --buffer-time=10000 -D plughw:CARD=CODEC,DEV=0 -t raw -r 11025 -f S16_LE | nc macos.example.com 23456

# MacOS command 1
# network -> MacOS virtual audio cable input (at PyAudio device 4)
nc -l 23456 | rig16-auout.py 1 4

# MacOS command 2
# MacOS received audio from virtual audiio cable output -> network
rig16-auin.py 1 4 | nc linux.example.com 23456

# Linux command 2
# nexwork -> Linux output to real device audio output
nc -l 23456 | aplay -D plughw:CARD=CODEC,DEV=0 --buffer-time=20000 -t raw -f S16_LE -r 11025 -c 1 -q -
