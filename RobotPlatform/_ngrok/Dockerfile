# based on: https://github.com/zaporylie/docker-rpi-ngrok

FROM ubuntu:bionic

RUN apt-get update && apt-get install -y \
    unzip \
    net-tools \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root

ADD https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip  ngrok.zip

RUN unzip ngrok.zip -d /bin \
 && rm -f ngrok.zip \
 && touch .ngrok

CMD /bin/ngrok http -config=.ngrok -log stdout --authtoken=$AUTHTOKEN --hostname=$NGROK_HOSTNAME $(netstat -nr | grep '^0\.0\.0\.0' | awk '{print $2}'):$HTTP_PORT
