#!/bin/bash
# Install Piper TTS binary
wget -q https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz
chmod +x piper/piper
cp piper/piper /usr/local/bin/
rm -rf piper*
echo "Piper installed!"