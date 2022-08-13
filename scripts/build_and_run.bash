#!/bin/bash
set -exu

# Can be executed from anywhere:
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
REPO_ROOT=$(git rev-parse --show-toplevel)
cd $REPO_ROOT


export OUTPUT=/dev/ttys000

date >$OUTPUT
source temp/p3-for-me/bin/activate
python wsock_ejector/wsock_ejector.py  1>$OUTPUT 2>$OUTPUT &

ps aux |grep wsock |grep -v grep

cd webapp
# webapp/package.json
npm install
npm run build
npm run watch

# python -m http.server
