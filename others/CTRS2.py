#!/usr/bin/python3
from bottle import route, run, template, request
import json
import urllib.request


tmp={
"name":"TI1",
"lang":"c",
"OS":"POSIX",
"tool": "gcc",
"segment": ["IOSS"],
"APIs": ["FACE_IO_Initialize","FACE_IO_Open","FACE_IO_Register","FACE_IO_Unregister","FACE_IO_Read","FACE_IO_Write","FACE_IO_Get_Status","FACE_IO_Close"]
}
@route('/')
def index():
    CT2aName = tmp["segment"]
    # find CT2a
    # call CT2a
    re = urllib.request.urlopen("http://192.168.0.156:9011").read()    
    return re

run(host='192.168.0.156', port=9010)
