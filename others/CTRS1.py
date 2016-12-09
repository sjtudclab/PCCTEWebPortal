#!/usr/bin/python3
from bottle import route, run, template, request

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
    location = request.query.location
    # download & parse
    # return json
    return tmp

run(host='192.168.0.156', port=9000)
