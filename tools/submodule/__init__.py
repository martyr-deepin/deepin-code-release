'''
submodule
'''

import argparse
import functools

from git_utils import (git_submodule_commit_to_tag,
                       git_submodule_latest_commit,
                       git_submodule_latest_tag,
                       git_submodule_get_commit,
                       git_submodule_list)

def register_module_args(subparsers):
    '''
    register_module_args
    '''
    parser = subparsers.add_parser("submodule",
                                   help="subcommand to deal with submodules in deepin-code-release")

    ssubparsers = parser.add_subparsers(title="submodule subcommand",
                                        help="subcommands that dcr submodule support.",
                                        dest="ssubcommand")

    status_parser = ssubparsers.add_parser("list",
                                           help="submodule subcommand to list all the submodules")

    status_parser = ssubparsers.add_parser("status",
                                           help="submodule subcommand to show the " \
                                                "current status of the submodules")
    status_parser.add_argument("--local", action="store_true",
                               help="output the local status of the submodules")
    status_parser.add_argument("--remote", action="store_true",
                               help="output the remote status of the submodules")
    status_parser.add_argument("--diff", action="store_true",
                               help="output the the difference between the local and the remote")
    status_parser.add_argument("submodules", nargs="*",
                               help="sepcify which submodule to operate on," \
                                    "default is all submodules")

def run_with_module_args(args):
    '''
    run_with_module_args
    '''
    if args.subcommand != __name__:
        return

    if args.ssubcommand == "status":
        if args.local:
            status_local(args.submodules)
        elif args.remote:
            status_remote(args.submodules)
        else:
            status_diff(args.submodules)
    elif args.ssubcommand == "list":
        list_all()

def list_all():
    '''
    list_all
    '''
    sbms = git_submodule_list()
    for sbm in sbms:
        print("%s" % sbm)

def status_local(projects):
    '''
    status_local
    '''
    sbms = git_submodule_list() if not projects else projects
    for sbm in sbms:
        tagify = lambda x, sbm=sbm: git_submodule_commit_to_tag(sbm, x) or x
        current_commit = git_submodule_get_commit(sbm)

        print("%s: %s" % (sbm, tagify(current_commit)))

def status_remote(projects):
    '''
    status_remote
    '''
    sbms = git_submodule_list() if not projects else projects
    for sbm in sbms:
        tagify = lambda x, sbm=sbm: git_submodule_commit_to_tag(sbm, x) or x
        latest_commit = git_submodule_latest_commit(sbm)
        latest_tag = git_submodule_latest_tag(sbm)

        print("%s: latest commit %s, latest tag %s" %
              (sbm, tagify(latest_commit), latest_tag))

def status_diff(projects):
    '''
    status
    '''
    sbms = git_submodule_list() if not projects else projects
    for sbm in sbms:
        tagify = lambda x, sbm=sbm: git_submodule_commit_to_tag(sbm, x) or x
        current_commit = git_submodule_get_commit(sbm)
        latest_commit = git_submodule_latest_commit(sbm)

        print("%s: current commit %s, remote latest commit %s." %
              (sbm, tagify(current_commit), tagify(latest_commit)))