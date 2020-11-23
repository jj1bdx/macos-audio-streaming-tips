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

## 48kHz Vorbis RTP stream over TCP

* Measured delay: ~0.2sec

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! "audio/x-raw,rate=48000" ! vorbisenc ! rtpvorbispay config-interval=1 ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```shell
# client and receiver macOS
gst-launch-1.0 tcpclientsrc port=5678 host=sender do-timestamp=true ! "application/x-rtp-stream,media=audio,clock-rate=48000,encoding-name=VORBIS" ! rtpstreamdepay ! rtpvorbisdepay ! decodebin ! audioconvert ! audioresample ! autoaudiosink
```

## Opus RTP stream

* Measured delay: ~0.2sec

```shell
# sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! audio/x-raw,channels=1 ! audiorate ! audioconvert ! opusenc bitrate=256000 frame-size=2.5 ! rtpopuspay ! udpsink host=receiver port=5008
```

```shell
# receiver macOS
gst-launch-1.0 udpsrc caps="application/x-rtp,channels=1" port=5008 ! rtpjitterbuffer latency=60 ! queue ! rtpopusdepay ! opusdec plc=true ! audioconvert ! audioresample ! autoaudiosink
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

## 44.1kHz linear PCM RTP stream over TCP

* Measured delay: ~0.1sec or lower
* Input sampling rate: 48kHz

### Linux -> macOS

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! audioconvert ! "audio/x-raw,rate=48000" ! audioresample ! "audio/x-raw,rate=44100" ! rtpL16pay ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```shell
# client and receiver macOS
gst-launch-1.0 tcpclientsrc port=5678 host=sender do-timestamp=true ! "application/x-rtp-stream,media=(string)audio, clock-rate=(int)44100, encoding-name=(string)L16, encoding-params=(string)2, channels=(int)2, payload=(int)96" ! rtpstreamdepay ! rtpL16depay ! audioconvert ! audioresample ! autoaudiosink buffer_time=20000 latency_time=10000
```

### macOS -> Linux (for the other direction)

Note: monitoring audio for this direction discovered that noticeable clicks (possibly phase disruption) were audible for every one second. (Timestamping issue?)

```
# server and sender macOS
gst-launch-1.0 -v osxaudiosrc device=130 provide-clock=true do-timestamp=true buffer-time=100000 ! audioconvert ! rtpL16pay ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```
# client and receiver Linux
gst-launch-1.0 -v tcpclientsrc port=5678 host=sender do-timestamp=true ! "application/x-rtp-stream,media=(string)audio, clock-rate=(int)44100, encoding-name=(string)L16, encoding-params=(string)2, channels=(int)2, payload=(int)96" ! rtpstreamdepay ! rtpL16depay ! audioconvert ! audioresample ! alsasink device=plughw:CARD=CODEC,DEV=0
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

## 44.1kHz linear PCM RTP stream over TCP, Payload Type 11 (monaural)

* Measured delay: ~0.1sec or lower
* Input sampling rate: 48kHz

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=hw:0,1 provide-clock=true do-timestamp=true buffer-time=40000 ! audioconvert mix-matrix="<<(float)0.5, (float)0.5>>" ! "audio/x-raw,rate=48000,channel=1" ! audioresample ! "audio/x-raw,rate=44100" ! rtpL16pay ! "application/x-rtp, media=audio, encoding-name=L16, payload=11,clock-rate=44100,channels=1" ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```shell
# client and receiver macOS
gst-launch-1.0 tcpclientsrc port=5678 host=sender do-timestamp=true ! "application/x-rtp-stream,media=audio, clock-rate=44100, encoding-name=L16, channels=1, payload=11" ! rtpstreamdepay ! rtpL16depay ! "audio/x-raw,rate=44100,channels=1" ! audioconvert ! audioresample ! autoaudiosink buffer_time=20000 latency_time=10000
```

## 44.1kHz linear PCM RTP stream over TCP, Payload Type 10 (stereo)

* Measured delay: ~0.1sec or lower
* Input sampling rate: 48kHz

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=hw:0,1 provide-clock=true do-timestamp=true buffer-time=40000 ! audioconvert ! "audio/x-raw,rate=48000,channel=2" ! audioresample ! "audio/x-raw,rate=44100" ! rtpL16pay ! "application/x-rtp, media=audio, encoding-name=L16, payload=10 ,clock-rate=44100,channels=2" ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```shell
# client and receiver macOS
gst-launch-1.0 tcpclientsrc port=5678 host=sender do-timestamp=true ! "application/x-rtp-stream, media=audio, clock-rate=44100, encoding-name=L16, channels=2, payload=10" ! rtpstreamdepay ! rtpL16depay ! "audio/x-raw,rate=44100, channels=2" ! audioconvert ! audioresample ! autoaudiosink buffer_time=20000 latency_time=10000
```
