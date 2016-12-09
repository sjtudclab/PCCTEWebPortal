#!/usr/bin/python
import urllib2
import json
re = urllib2.urlopen("http://192.168.0.156:9000/").read()
print(re)
re = urllib2.urlopen("http://192.168.0.156:9010/").read()
print(re)
