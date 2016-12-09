#!/usr/bin/python3
from bottle import route, run, template, request
import json
import subprocess

tmp={
"name":"TI1",
"lang":"c",
"OS":"POSIX",
"tool": "gcc",
"segment": ["IOSS"],
"APIs": ["FACE_IO_Initialize","FACE_IO_Open","FACE_IO_Register","FACE_IO_Unregister","FACE_IO_Read","FACE_IO_Write","FACE_IO_Get_Status","FACE_IO_Close"]
}
@route('/')#, method=['GET','POST'])
def index():
    CT2aName = tmp["segment"]
    # parse test plan
    # execute
    try:
        compilePhase=subprocess.check_output('gcc -c main.cpp ', stderr=subprocess.STDOUT,shell=True).decode('utf-8')
        linkerPhase=subprocess.check_output('gcc -o main main.o IOS.o', stderr=subprocess.STDOUT, shell=True).decode('utf-8')
        outputPhase = compilePhase + linkerPhase
    except Exception as e:
        print(e)
        outputPhase = str(e.output)
    return 'True'+ outputPhase 


run(host='0.0.0.0', port=9011)
