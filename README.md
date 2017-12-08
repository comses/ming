# ming
Modeling in the Next Generation.

This is an example of coupling a hydrology model that routes water across a landscape with the DSSAT crop model.

## requirements

Install [docker and docker-compose](https://docs.docker.com/compose/install/). To run dssat on a pile of weather station
files, symlink or move those files into `./data/incoming/` (they must sit directly within that folder, we don't
recursively search for WTH files).

In order to be processed, the generated weather station files are expected to be of the format `USAM8031_<grid_id>.WTH`
where `grid_id` is an integer between 1-99999 (5 digits max). We could easily support larger numbers by changing how we
update the dssat template.mzx file to generate a new MZX referencing the renamed WTH file. For more information on DSSAT
MZX files see the [DSSAT User's Guide vol 3](https://dssat.net/wp-content/uploads/2011/10/DSSAT-vol3.pdf).

## run instructions

```
% docker-compose build --pull # build the ming Docker image
% docker-compose run --rm ming bash # to explore the Docker image
container> ./process.py /data/test
container> ./process.py /data/incoming
```

For brevity if you symlink or copy your files into `./data/incoming` you can simply run `docker-compose run --rm ming`
and it should begin processing all the WTH files you placed in `./data/incoming`. Results are stored in `src/results` at
the moment.

## build status
[![Build Status](https://travis-ci.org/comses/ming.svg?branch=master)](https://travis-ci.org/comses/ming)


