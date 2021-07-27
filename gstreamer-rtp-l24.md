# RTP L24 stream

* Rate conversion from 48kHz to 44.1kHz performed

## sender Linux

```shell
gst-launch-1.0 alsasrc device=hw:0,1 provide-clock=true do-timestamp=true buffer-time=20000 ! audioconvert ! queue ! "audio/x-raw,rate=48000" ! audioresample ! queue ! "audio/x-raw,rate=44100" ! rtpL24pay ! udpsink host=receiver port=5108
```

## receiver macOS

```shell
gst-launch-1.0 udpsrc port=5108 caps="application/x-rtp,media=audio,payload=96,clock-rate=44100,encoding-name=L24,channels=2" ! rtpjitterbuffer latency=30 ! rtpL24depay ! queue ! audioconvert ! audioresample ! osxaudiosink device=66 buffer_time=20000 latency_time=10000
```
