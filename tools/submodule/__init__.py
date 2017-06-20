'''
submodule
'''

import argparse
import functools

from git_utils import (git_submodule_commit_to_tag,
                       git_submodule_latest_commit,
                       git_submodule_latest_tag,
                       git_submodule_get_commit,
                       git_submodule_set_commit,
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

    _ = ssubparsers.add_parser("list",
                               help="submodule subcommand to list all the submodules")

    sync_parser = ssubparsers.add_parser("sync",
                                         help="submodule subcommand to sync submodule local ref " \
                                              "to the remote latest tag")
    sync_parser.add_argument("submodules", nargs="*",
                             help="sepcify which submodule to operate on," \
                                  "default is all submodules")

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
    elif args.ssubcommand == "sync":
        sync(args.submodules)

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
    delimiter="  |  "
    name_maxlen=max((len(n) for n in sbms))
    table_head = "{:{name_maxlen}}{delimiter}{}".format(
        "project", "tag", name_maxlen=name_maxlen, delimiter=delimiter)
    print(table_head, "="*(len(table_head)+5), sep="\n")

    for sbm in sbms:
        tagify = lambda x, sbm=sbm: git_submodule_commit_to_tag(sbm, x) or x
        current_commit = git_submodule_get_commit(sbm)
        tagified = tagify(current_commit)
        print("{sbm:{name_maxlen}}{delimiter}{tagified}".format_map(locals()))

def status_remote(projects):
    '''
    status_remote
    '''
    sbms = git_submodule_list() if not projects else projects
    delimiter="  |  "
    name_maxlen=max((len(n) for n in sbms))

    table_head = "{0:{name_maxlen}}{delimiter}{1:40}{delimiter}{2}".format(
        "project", "latest_commit", "latest_tag", name_maxlen=name_maxlen, delimiter=delimiter)
    print(table_head, "="*len(table_head), sep="\n")

    for sbm in sbms:
        tagify = lambda x, sbm=sbm: git_submodule_commit_to_tag(sbm, x) or x
        latest_commit = git_submodule_latest_commit(sbm)
        tagified = tagify(latest_commit)
        latest_tag = git_submodule_latest_tag(sbm)
        print("{sbm:{name_maxlen}}{delimiter}{tagified:40}{delimiter}{latest_tag}".format_map(locals()))

def status_diff(projects):
    '''
    status
    '''
    sbms = git_submodule_list() if not projects else projects
    for sbm in sbms:
        tagify = lambda x, sbm=sbm: git_submodule_commit_to_tag(sbm, x) or x
        current_commit = tagify(git_submodule_get_commit(sbm))
        latest_tag = git_submodule_latest_tag(sbm)

        if current_commit != latest_tag:
            print("%s: \n\tlocal current     %s\n\tremote latest tag %s" %
                  (sbm, current_commit, latest_tag))


def sync(projects):
    '''
    status
    '''
    sbms = git_submodule_list() if not projects else projects
    for sbm in sbms:
        tagify = lambda x, sbm=sbm: git_submodule_commit_to_tag(sbm, x) or x
        current_commit = tagify(git_submodule_get_commit(sbm))
        latest_tag = git_submodule_latest_tag(sbm)

        if current_commit != latest_tag:
            print("%s: checkout to %s from %s" %
                  (sbm, latest_tag, current_commit))
            git_submodule_set_commit(sbm, latest_tag)
