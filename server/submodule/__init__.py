'''
submodule
'''

import argparse
import functools

from git_utils import *


def _status_one(module_name):
    '''
    _status_one
    '''
    info = {}

    current_commit = git_submodule_get_commit(module_name)
    latest_commit = git_submodule_latest_commit(module_name)
    latest_tag = git_submodule_latest_tag(module_name)

    info["name"] = module_name
    info["locale"] = {
        "commit": current_commit,
        "tag": git_submodule_commit_to_tag(module_name, current_commit)
    }
    info["origin"] = {
        "latest_commit": latest_commit,
        "latest_tag": latest_tag,
        "steps": git_submodule_commit_minus_tag(module_name,
                                                latest_commit, latest_tag)
    }

    return info

def status_one(module_name):
    '''
    status_one
    '''
    sbms = git_submodule_list()
    if module_name in sbms:
        return _status_one(module_name)
    else:
        return None

def status_all():
    '''
    status_all
    '''

    sbms = git_submodule_list()

    result = []

    for sbm in sbms:
        info = _status_one(sbm)
        result.append(info)

    return result
