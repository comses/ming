FROM comses/dssat:4.6.6

LABEL maintainer="Allen Lee <allen.lee@asu.edu>"

RUN apt-get update && apt-get install -y \
    python3-pip

WORKDIR /code/run
COPY . /code/ming
