#!/bin/bash

rm -rf /code/run/results.old
mv -fT /code/run/results{,.old}
chmod a+x /code/run/run.py
/code/run/run.py /data/test
