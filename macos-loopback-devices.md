# Usable macOS loopback devices

## Expected usage

* Live audio streaming between macOS and Linux
* Minimum latency
* Relaying macOS WSJT-X audio I/O to a Raspberry Pi Linux audio I/O

## Installed drivers path on macOS

/Library/Audio/Plug-Ins/HAL

## How to restart CoreAudio daemon

```shell
sudo launchctl kickstart -kp system/com.apple.audio.coreaudiod
```

## Paid products

* [Rogue Amoeba Loopback](https://rogueamoeba.com/loopback/)
  - Worth paying the price of USD109/license key
  - No problem without PortAudio input/output
  - No problem for gstreamer input/output
  - Able to instantly create/delete loopback devices with arbitrary names
  - Able to monitor loopback devices separately for each device

## Free software

* [Blackhole](https://github.com/ExistentialAudio/BlackHole)
  - Single loopback device only (by the installer)
  - Unable to run multiple instance even with recompilation yet
  - No problem without PortAudio input/output
  - No problem for gstreamer input/output

## Not usable for my purposes

* [dl1ycf/MacOSVirtualAudio](https://github.com/dl1ycf/MacOSVirtualAudio): kext, not for my purpose
* [elements-storage/AudioLoopback](https://github.com/elements-storage/AudioLoopback): looks promising (using HAL), but unable to activate

