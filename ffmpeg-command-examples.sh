# RTP transmission in 48kHz 192kbps stereo MP3
# Sender at sender.example.com
arecord --buffer-time=10000 -D plughw:CARD=CODEC,DEV=0 -f S16_LE -c2 -r48000 | ffmpeg -vn -re -i - -acodec libmp3lame -ar 48000 -ab 192k -ac 2 -f rtp rtp://receiver.example.com:34567
# receiver at receiver.example.com
ffmpeg -i rtp://receiver.example.com:34567 -f s16le - | r16auout.py 2
