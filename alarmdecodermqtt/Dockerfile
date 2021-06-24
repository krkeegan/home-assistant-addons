ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_VERSION
ARG BUILD_ARCH

# Add env
ENV LANG C.UTF-8

COPY . /opt/alarmdecoder

# Setup base
RUN apk --no-cache add python3-dev
RUN cd /opt/alarmdecoder/alarmdecoder \
  && python3 setup.py

COPY run.sh /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
