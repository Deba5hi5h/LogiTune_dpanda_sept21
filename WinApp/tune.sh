#!/bin/bash
if [ -d "/Applications/LogiTune.app" ]; then
    open "/Applications/LogiTune.app" --args --remote-debugging-port=$1
elif [ -d "/Applications/Logi Tune.app" ]; then
    open "/Applications/Logi Tune.app" --args --remote-debugging-port=$1
else
    echo "App not found"
fi