#!/bin/bash
tmux kill-session -t flask
git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt

tmux new -d -s flask "flask run --host 0.0.0.0"
echo "Re-deployed application"
