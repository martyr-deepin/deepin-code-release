#!/usr/bin/env python3

'''
server.py is the server implementation to manipulate deepin-code-release
through the web interface.
'''

import json

from flask import Flask, request, abort

import submodule
from errors import GitException

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

@APP.route("/submodule/<module_name>", methods=["GET", "POST"])
def submodules_one(module_name):
    '''
    manipulate on the specific one submodule
    '''
    if request.method == "GET":
        data = submodule.status_one(module_name)
        if data:
            return json.dumps(data)
        else:
            abort(404)
    elif request.method == "POST":
        print(request.form["commit"])
        try:
            commit = request.form["commit"]
            submodule.update_one(module_name, commit)
            return "success"
        except GitException as ex:
            print(ex)
            return "failed"


if __name__ == "__main__":
    APP.run()
