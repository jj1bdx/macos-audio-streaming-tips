# gstreamer streaming examples

## Note

* Sender Linux: Raspberry Pi 4B with Raspberry Pi OS
* Receiver macOS: macOS 10.15.7

## Note for macOS

### osxaudiosrc and osxaudiosink

* Use `osxaudiosrc` for OSX device input
* Use `osxaudiosink` for OSX device output
* Use as `osxaudiosink device=93`
* To obtain devices, install [macos-audio-devices](https://github.com/karaggeorge/macos-audio-devices)

## 48kHz Vorbis RTP stream over TCP

Measured delay: ~0.2sec

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! "audio/x-raw,rate=48000" ! vorbisenc ! rtpvorbispay config-interval=1 ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```shell
# client and receiver macOS
gst-launch-1.0 tcpclientsrc port=5678 host=sender do-timestamp=true ! "application/x-rtp-stream,media=audio,clock-rate=48000,encoding-name=VORBIS" ! rtpstreamdepay ! rtpvorbisdepay ! decodebin ! audioconvert ! audioresample ! autoaudiosink
```

## Opus RTP stream 

Measured delay: ~0.2sec

```shell
# sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! audio/x-raw,channels=1 ! audiorate ! audioconvert ! opusenc bitrate=256000 frame-size=2.5 ! rtpopuspay ! udpsink host=receiver port=5008
```

```shell
# receiver macOS
gst-launch-1.0 udpsrc caps="application/x-rtp,channels=1" port=5008 ! rtpjitterbuffer latency=60 ! queue ! rtpopusdepay ! opusdec plc=true ! audioconvert ! audioresample ! autoaudiosink
```

## 8kHz ALAW RTP stream over TCP

Measured delay: ~0.1sec or lower

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! audioconvert ! alawenc ! rtppcmapay ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```shell
# client and receiver macOS
gst-launch-1.0 tcpclientsrc port=5678 host=***REMOVED*** do-timestamp=true ! "application/x-rtp-stream,media=(string)audio,clock-rate=(int)8000,encoding-name=(string)PCMA" ! rtpstreamdepay ! rtppcmadepay ! alawdec ! audioconvert ! audioresample ! autoaudiosink buffer_time=20000 latency_time=10000
```

## 44.1kHz linear PCM RTP stream over TCP

* Measured delay: ~0.1sec or lower

### Linux -> macOS

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! audioconvert ! rtpL16pay ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```shell
# client and receiver macOS
gst-launch-1.0 tcpclientsrc port=5678 host=***REMOVED*** do-timestamp=true ! "application/x-rtp-stream,media=(string)audio, clock-rate=(int)44100, encoding-name=(string)L16, encoding-params=(string)2, channels=(int)2, payload=(int)96" ! rtpstreamdepay ! rtpL16depay ! audioconvert ! audioresample ! autoaudiosink buffer_time=20000 latency_time=10000
```

### macOS -> Linux (for the other direction)

```
# server and sender macOS
gst-launch-1.0 -v osxaudiosrc device=130 provide-clock=true do-timestamp=true buffer-time=100000 ! audioconvert ! rtpL16pay ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```
# client and receiver Linux
gst-launch-1.0 -v tcpclientsrc port=5678 host=sender do-timestamp=true ! "application/x-rtp-stream,media=(string)audio, clock-rate=(int)44100, encoding-name=(string)L16, encoding-params=(string)2, channels=(int)2, payload=(int)96" ! rtpstreamdepay ! rtpL16depay ! audioconvert ! audioresample ! alsasink device=plughw:CARD=CODEC,DEV=0
```
