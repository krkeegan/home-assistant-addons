ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_VERSION
ARG BUILD_ARCH

# Add env
ENV LANG C.UTF-8

# Setup base
RUN cd /opt/alarmdecoder/alarmdecoder \
  && python setup.py

COPY run.sh /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
