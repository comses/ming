# ming
Modeling in the Next Generation.

This is an example of coupling a hydrology model that routes water across a landscape with the DSSAT crop model.

## run it

Install [docker and docker-compose](https://docs.docker.com/compose/install/) then run

```
% docker-compose build --pull # build the ming Docker image
% docker-compose run --rm ming bash
container> ./run.py /data/test
container> ./run.py /data/<actual-input-directory-with-65536-wth-files>

## build status
[![Build Status](https://travis-ci.org/comses/ming.svg?branch=master)](https://travis-ci.org/comses/ming)
```

