#!/bin/bash

test -f /code/run/results.old && rm -rf /code/run/results.old
test -f /code/run/results && mv -fT /code/run/results{,.old}
chmod a+x /code/run/process.py
/code/run/process.py /data/test
