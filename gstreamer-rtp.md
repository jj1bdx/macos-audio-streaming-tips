## gstreamer streaming examples

### Note

* Sender Linux: Raspberry Pi 4B with Raspberry Pi OS
* Receiver macOS: macOS 10.15.7

### 48kHz Vorbis RTP stream over TCP

Measured delay: ~0.2sec

```shell
# server and sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! "audio/x-raw,rate=48000" ! vorbisenc ! rtpvorbispay config-interval=1 ! rtpstreampay ! tcpserversink port=5678 host=sender
```

```shell
# client and receiver macOS
gst-launch-1.0 tcpclientsrc port=5678 host=sender do-timestamp=true ! "application/x-rtp-stream,media=audio,clock-rate=48000,encoding-name=VORBIS" ! rtpstreamdepay ! rtpvorbisdepay ! decodebin ! audioconvert ! audioresample ! autoaudiosink
```

### Opus RTP stream 

```shell
# sender Linux
gst-launch-1.0 alsasrc device=plughw:CARD=CODEC,DEV=0 provide-clock=true do-timestamp=true buffer-time=20000 ! audio/x-raw,channels=1 ! audiorate ! audioconvert ! opusenc bitrate=256000 frame-size=2.5 ! rtpopuspay ! udpsink host=receiver port=5008
```

```shell
# receiver macOS
gst-launch-1.0 -v udpsrc caps="application/x-rtp,channels=1" port=5008 ! rtpjitterbuffer latency=60 ! queue ! rtpopusdepay ! opusdec plc=true ! audioconvert ! audioresample ! autoaudiosink
```
