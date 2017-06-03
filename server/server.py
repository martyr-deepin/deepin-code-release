#!/usr/bin/env python3

'''
server.py is the server implementation to manipulate deepin-code-release
through the web interface.
'''

import json

from flask import Flask

import submodule

APP = Flask("dcr-server")

@APP.route("/")
def index():
    '''
    show greetings for now.
    '''
    return "Welcome to the dcr-server!"

@APP.route("/submodule/")
def submodules_all():
    '''
    list all submodules and the status information related.
    '''
    data = submodule.status_all()
    return json.dumps(data)

@APP.route("/submodule/<module_name>")
def submodules_one(module_name):
    '''
    show the status of the submodule specified by parameter submodule
    '''
    data = submodule.status_one(module_name)
    return json.dumps(data)


if __name__ == "__main__":
    APP.run()
