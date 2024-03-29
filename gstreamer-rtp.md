# gstreamer streaming examples

## System configuration

* Sender Linux: Raspberry Pi 4B with Raspberry Pi OS
* Receiver macOS: macOS 10.15.7

## Note for macOS

### osxaudiosrc and osxaudiosink

* Use `osxaudiosrc` for OSX device input
* Use `osxaudiosink` for OSX device output
* Use as `osxaudiosink device=93`
* To obtain devices, install [macos-audio-devices](https://github.com/karaggeorge/macos-audio-devices)

## 44.1kHz stereo linear PCM over UDP

* [RTP payload format](https://en.wikipedia.org/wiki/RTP_payload_formats) Type 10

### Linux -> macOS

* Use plughw if resampling is required

```shell
# client and sender Linux
gst-launch-1.0 alsasrc device=hw:4,0 provide-clock=true do-timestamp=true buffer-time=40000 ! "audio/x-raw,rate=44100" ! audioconvert ! rtpL16pay ! "application/x-rtp, media=audio, encoding-name=L16, payload=10 ,clock-rate=44100,channels=2" ! udpsink host=receiver port=5008
```

```shell
# server and receiver macOS
gst-launch-1.0 udpsrc port=5008 caps="application/x-rtp,media=(string)audio, clock-rate=(int)44100, encoding-name=(string)L16, encoding-params=(string)2, channels=(int)2, payload=(int)10" ! rtpjitterbuffer latency=30 ! queue ! rtpL16depay ! audioconvert ! osxaudiosink device=44 buffer_time=20000 latency_time=10000
```

### macOS -> Linux

* Resample needed on the sender side of OSX Audio

```shell
# client and sender macOS
gst-launch-1.0 -v osxaudiosrc device=55 buffer-time=100000 ! audioconvert ! audioresample ! "audio/x-raw,rate=44100" ! rtpL16pay ! "application/x-rtp, media=audio, encoding-name=L16, payload=10 ,clock-rate=44100,channels=2" ! udpsink host=receiver port=5008
```

```shell
# server and receiver Linux
gst-launch-1.0 udpsrc port=5008 caps="application/x-rtp,media=(string)audio, clock-rate=(int)44100, encoding-name=(string)L16, encoding-params=(string)2, channels=(int)2, payload=(int)10" ! rtpjitterbuffer latency=30 ! queue ! rtpL16depay ! audioconvert ! alsasink device=plughw:CARD=UA22,DEV=0
```

## 48kHz Vorbis RTP stream over TCP

* Measured delay: ~0.2sec

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=hw:0,1 provide-clock=true do-timestamp=true buffer-time=60000 ! audioconvert ! queue ! "audio/x-raw,rate=48000,channel=2" ! vorbisenc ! queue ! rtpvorbispay config-interval=1 ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```shell
# client and receiver macOS
gst-launch-1.0 tcpclientsrc port=5678 host=sender do-timestamp=true ! "application/x-rtp-stream, media=audio, clock-rate=48000, encoding-name=VORBIS" ! rtpstreamdepay ! queue ! rtpvorbisdepay ! queue ! decodebin ! audioconvert ! audioresample ! autoaudiosink buffer_time=50000 latency_time=10000
```

## Opus RTP stream

* Measured delay: ~0.2sec

```shell
# sender Linux
gst-launch-1.0 alsasrc device=hw:6,0 provide-clock=true do-timestamp=true buffer-time=40000 ! audio/x-raw,channels=1 ! audiorate ! audioconvert ! opusenc bitrate=64000 frame-size=2.5 ! rtpopuspay ! udpsink host=receiver port=5108
```

```shell
# receiver macOS
gst-launch-1.0 udpsrc port=5108 caps="application/x-rtp,channels=1" ! rtpjitterbuffer latency=60 ! queue ! rtpopusdepay ! queue ! opusdec plc=true ! audioconvert ! audioresample ! osxaudiosink device=66 buffer_time=20000 latency_time=10000
```

## 8kHz A-Law RTP stream over TCP

* Measured delay: ~0.1sec or lower
* Note: using TCP might have caused cumulative latency for long-time streaming (about 2 hours)

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! audioconvert ! alawenc ! rtppcmapay ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```shell
# client and receiver macOS
gst-launch-1.0 tcpclientsrc port=5678 host=sender do-timestamp=true ! "application/x-rtp-stream,media=(string)audio,clock-rate=(int)8000,encoding-name=(string)PCMA" ! rtpstreamdepay ! rtppcmadepay ! alawdec ! audioconvert ! audioresample ! autoaudiosink buffer_time=20000 latency_time=10000
```

## 8kHz A-Law RTP over UDP

* Measured delay: ~0.1sec or lower

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! audioconvert ! alawenc ! rtppcmapay ! udpsink host=receiver port=5008
```

```shell
# client and receiver macOS
gst-launch-1.0 udpsrc caps="application/x-rtp,media=(string)audio,clock-rate=(int)8000,encoding-name=(string)PCMA" port=5008 ! rtpjitterbuffer latency=60 ! queue ! rtppcmadepay ! alawdec ! audioconvert ! audioresample ! osxaudiosink device=62 buffer_time=20000 latency_time=10000
```

## 48kHz -> 44.1kHz linear PCM RTP over UDP

* Measured delay: ~0.1sec or lower
* RTP only accepts 44.1kHz S16BE mono or stereo

### Linux -> macOS

```shell
# client and sender Linux
gst-launch-1.0 alsasrc device=hw:0,1 provide-clock=true do-timestamp=true buffer-time=40000 ! "audio/x-raw,rate=48000" ! audioresample ! "audio/x-raw,rate=44100" ! audioconvert ! rtpL16pay ! udpsink host=receiver port=5008
```

```shell
# server and receiver macOS
gst-launch-1.0 udpsrc port=5008 caps="application/x-rtp,media=(string)audio, clock-rate=(int)44100, encoding-name=(string)L16, encoding-params=(string)2, channels=(int)2, payload=(int)96" ! rtpjitterbuffer latency=30 ! queue ! rtpL16depay ! audioconvert ! audioresample ! osxaudiosink device=62 buffer_time=20000 latency_time=10000
```

### Linux -> macOS version 2 (modified)

```shell
# client and sender Linux
gst-launch-1.0 alsasrc device=hw:0,1 provide-clock=true do-timestamp=true buffer-time=40000 ! queue ! "audio/x-raw,rate=48000" ! audioresample ! "audio/x-raw,rate=44100" ! audioconvert ! queue ! rtpL16pay ! udpsink host=receiver port=5008
```

```shell
# server and receiver macOS
gst-launch-1.0 udpsrc port=5008 caps="application/x-rtp,media=(string)audio, clock-rate=(int)44100, encoding-name=(string)L16, encoding-params=(string)2, channels=(int)2, payload=(int)96" ! rtpjitterbuffer latency=30 ! queue ! rtpL16depay ! audioconvert ! queue ! audioresample ! osxaudiosink device=77 buffer_time=20000 latency_time=10000
```

