# ffmpeg streaming examples

## Note

* Audio latency measured via ethernet: ~700msec
* *Still unable to find an option to shorten the audio latency*
* Sender Linux: Raspberry Pi 4B with Raspberry Pi OS
* Receiver macOS: macOS 10.15.7
* ffplay does not recognize non-native RTP payload types. See [Wikipedia RTP Payload Type list](https://en.wikipedia.org/wiki/RTP_payload_formats) for the native format types.

## 48kHz 256kbps MP3 stereo RTP

```shell
# sender Linux
arecord --buffer-time=10000 -D plughw:CARD=CODEC,DEV=0 -f S16_LE -c2 -r48000 | ffmpeg -probesize 32 -fflags nobuffer -f s16le -sample_rate 48000 -channels 2 -vn -re -i - -codec libmp3lame -ar 48000 -ab 256k -ac 2 -f rtp rtp://receiver:34567
```

```shell
# receiver macOS
ffmpeg -probesize 32 -fflags nobuffer -fflags discardcorrupt -flags low_delay -avioflags direct -i rtp://receiver:34567 -f s16le - | r16auout.py 2
```

## 44.1kHz linear PCM mono RTP

```shell
# sender Linux
arecord --buffer-time=10000 -D plughw:CARD=CODEC,DEV=0 -f S16_LE -c1 -r44100 | ffmpeg -probesize 32 -fflags nobuffer -f s16le -sample_rate 44100 -channels 1 -vn -re -i - -acodec pcm_s16be -ar 44100 -ac 1 -f rtp rtp://receiver:34567
```

```shell
# receiver macOS
ffmpeg -probesize 32 -fflags nobuffer -fflags discardcorrupt -flags low_delay -avioflags direct -i rtp://receiver:34567 -f s16le - | r16-44100-auout.py 1
```

## 16kHz g.722 mono RTP

```shell
# sender Linux
arecord --buffer-time=10000 -D plughw:CARD=CODEC,DEV=0 -f S16_LE -c1 -r16000 | ffmpeg -probesize 32 -fflags nobuffer -f s16le -sample_rate 16000 -channels 1 -vn -re -i - -acodec g722 -ar 16000 -ac 1 -f rtp rtp://receiver:34567
```

```shell
# receiver macOS
ffplay -probesize 32 -fflags nobuffer -fflags discardcorrupt -flags low_delay -avioflags direct -i rtp://receiver:34567
```

## 16kHz g.722 mono with RTSP SDP TCP transport

```shell
# sender Linux
arecord --buffer-time=10000 -D plughw:CARD=CODEC,DEV=0 -f S16_LE -c1 -r16000 | ffmpeg -probesize 32 -fflags nobuffer -f s16le -sample_rate 16000 -channels 1 -vn -re -i - -acodec g722 -ar 16000 -ac 1 -f rtsp -rtsp_transport tcp rtsp://receiver:45678/live.sdp
```

```shell
# receiver macOS
ffplay -nodisp -probesize 32 -fflags nobuffer -fflags discardcorrupt -flags low_delay -avioflags direct -rtsp_flags listen "rtsp://receiver:45678/live.sdp"
```

## 44.1kHz linear PCM stereo with RTSP SDP TCP transport

```shell
# sender Linux
arecord --buffer-time=20000 -D plughw:CARD=CODEC,DEV=0 -f S16_LE -c2 -r44100 | ffmpeg -probesize 32 -fflags nobuffer -f s16le -sample_rate 44100 -channels 2 -vn -re -i - -acodec pcm_s16be -bufsize 100k -ar 44100 -ac 2 -f rtsp -rtsp_transport tcp rtsp://receiver:45678/live.sdp
```

```shell
# receiver macOS
ffplay -nodisp -probesize 32 -fflags nobuffer -fflags discardcorrupt -flags low_delay -avioflags direct -rtsp_flags listen rtsp://receiver:45678/live.sdp
```

## 48kHz 256kbps MPEG-1 Layer 2 (MP2) stereo with RTSP SDP TCP transport

* For lower CPU load

```shell
# sender Linux
arecord --buffer-time=10000 -D plughw:CARD=CODEC,DEV=0 -f S16_LE -c2 -r48000 | ffmpeg -probesize 32 -fflags nobuffer -f s16le -sample_rate 48000 -channels 2 -vn -re -i - -codec mp2 -ar 48000 -ab 256k -ac 2 -f rtsp -rtsp_transport tcp rtsp://receiver:45678/live.sdp
```

```shell
# receiver macOS
ffmpeg -probesize 32 -fflags nobuffer -fflags discardcorrupt -flags low_delay -avioflags direct -rtsp_flags listen -i rtsp://receiver:45678/live.sdp -f s16le - | r16auout.py 2
```
