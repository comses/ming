# ming
Modeling in the Next Generation.

This is an example of coupling a hydrology model that routes water across a landscape with the DSSAT crop model.

## running it

Install [docker and docker-compose](https://docs.docker.com/compose/install/) then run

```
% docker-compose build # build the dssat Docker image
% docker-compose up -d
% docker-compose exec dssat bash
<inside the dssat container>% cd dssat 
<inside the dssat container>% dssat A ARAM8001.MZX
```
