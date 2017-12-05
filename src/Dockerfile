FROM comses/dssat:4.6.6

LABEL maintainer="Allen Lee <allen.lee@asu.edu>"

RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-pip \
    && chmod a+x /usr/local/bin/dscsm046.exe

WORKDIR /code/run
COPY . /code/run
