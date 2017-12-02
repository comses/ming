#!/bin/bash

mv /code/run/results{,.old}
chmod a+x /code/run/run.py
/code/run/run.py /data/test
