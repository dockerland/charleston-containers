FROM alpine:3.4

RUN apk add --no-cache py-tornado py-pip &&\
  pip install hvac

COPY server.py /run/server.py
EXPOSE 8888
CMD /run/server.py
