# Opus RTP stream

## sender Linux

```shell
gst-launch-1.0 alsasrc device=hw:0,1 provide-clock=true do-timestamp=true buffer-time=40000 ! audioconvert ! audioresample ! opusenc bitrate=64000 frame-size=2.5 ! rtpopuspay ! udpsink host=receiver port=5108
```

## receiver macOS

```shell
gst-launch-1.0 udpsrc port=5108 caps="application/x-rtp" ! rtpjitterbuffer latency=60 ! queue ! rtpopusdepay ! queue ! opusdec ! audioconvert ! audioresample ! osxaudiosink device=66 buffer_time=20000 latency_time=10000
```
