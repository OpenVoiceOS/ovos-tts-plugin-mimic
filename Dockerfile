FROM debian:buster-slim

RUN apt-get update && \
  apt-get install -y git python3 python3-dev python3-pip portaudio19-dev curl build-essential

RUN curl https://forslund.github.io/mycroft-desktop-repo/mycroft-desktop.gpg.key | \
  apt-key add - 2>/dev/null && \
  echo "deb http://forslund.github.io/mycroft-desktop-repo bionic main" \
  > /etc/apt/sources.list.d/mycroft-mimic.list && \
  apt-get update && \
  apt-get install -y mimic && \
  apt-get -y autoremove && \
  apt-get clean


RUN pip3 install ovos-utils==0.0.15
RUN pip3 install ovos-plugin-manager==0.0.4
RUN pip3 install ovos-tts-server==0.0.2

COPY . /tmp/ovos-tts-plugin-mimic
RUN pip3 install /tmp/ovos-tts-plugin-mimic

ENTRYPOINT ovos-tts-server --engine ovos-tts-plugin-mimic