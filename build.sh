#!/bin/sh
# zostavenie stránky: src/base.html + src/3d.js → index.html (verzia pre GitHub Pages s ukladaním do vetvy "data")
set -e
cd "$(dirname "$0")"
python3 src/patch.py src/base.html /tmp/byt-artifact.html
python3 src/ghpatch.py /tmp/byt-artifact.html index.html
