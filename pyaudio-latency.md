# Latency issues of PyAudio

* PyAudio output latency is manageable
* PyAudio *input latency is not manageable*, especially for lower sampling rates

## Possible workarounds

* Rewrite all PyAudio scripts by C/C++, i.e., rewriting them by PortAudio
