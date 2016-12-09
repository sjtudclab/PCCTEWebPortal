
FROM ubuntu:14.04
MAINTAINER Kevin Lui "kevinlui598@gmail.com"
RUN apt-get update
RUN apt-get install -y gcc
COPY ./ .
EXPOSE 9011
CMD []
ENTRYPOINT ["/usr/bin/python3", "CTRS2aIOSSCT.py&"]