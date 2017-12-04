#!/bin/sh

cut -b20-37 < $1 | tail -n1 | tr -s ' '
