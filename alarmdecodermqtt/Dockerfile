ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_VERSION
ARG BUILD_ARCH

# Add env
ENV LANG C.UTF-8

COPY . /opt/alarmdecoder

# Setup base
RUN apk --no-cache add python3-dev py3-pip
RUN pip3 install setuptools
RUN cd /opt/alarmdecoder/alarmdecoder \
  && python3 setup.py install

COPY run.sh /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
