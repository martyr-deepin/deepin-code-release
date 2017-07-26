'''
submodule
'''

import argparse
import functools

from git_utils import RepoManager, SubmoduleError, TagError

repo = RepoManager(".")

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
    sbms = repo.submodule_list
    for sbm in sbms:
        print("%s" % sbm)

def status_local(projects):
    '''
    status_local
    '''
    sbms = repo.get_all_submodules() if not projects else projects
    delimiter="  |  "
    name_maxlen=max((len(m.name) for m in sbms))
    table_head = "{:{name_maxlen}}{delimiter}{}".format(
        "project", "tag", name_maxlen=name_maxlen, delimiter=delimiter)
    print(table_head, "="*(len(table_head)+5), sep="\n")

    for sbm in sbms:
        print("{sbm.name:{name_maxlen}}{delimiter}{sbm.latest_tag}".format_map(locals()))

def status_remote(projects):
    '''
    status_remote
    '''
    sbms = repo.get_all_submodules() if not projects else projects
    delimiter="  |  "
    name_maxlen=max((len(m.name) for m in sbms))

    table_head = "{0:{name_maxlen}}{delimiter}{1:40}{delimiter}{2}".format(
        "project", "latest_commit", "latest_tag", name_maxlen=name_maxlen, delimiter=delimiter)
    print(table_head, "="*len(table_head), sep="\n")

    for sbm in sbms:
        name = sbm.name
        latest_commit = sbm.latest_origin_commit
        try:
            tagified = sbm.commit_to_tag(latest_commit).name
        except TagError:
            tagified = latest_commit
        latest_tag = sbm.latest_tag
        print("{name:{name_maxlen}}{delimiter}{tagified:40}{delimiter}{latest_tag}".format_map(locals()))

def status_diff(projects):
    '''
    status
    '''
    sbms = repo.get_all_submodules() if not projects else projects
    for sbm in sbms:
        current_commit = sbm.latest_commit
        try:
            tagified = sbm.commit_to_tag(current_commit).name
        except TagError:
            tagified = current_commit
        latest_tag = sbm.latest_tag.name

        if tagified != latest_tag:
            print("%s: \n\tlocal current     %s\n\tremote latest tag %s" %
                  (sbm.name, tagified, latest_tag))


def sync(projects):
    '''
    status
    '''
    sbms = repo.get_all_submodules() if not projects else projects
    for sbm in sbms:
        current_commit = sbm.latest_commit
        try:
            tagified = sbm.commit_to_tag(current_commit).name
        except TagError:
            tagified = current_commit
        latest_tag = sbm.latest_tag.name

        if tagified != latest_tag:
            print("%s: %s -> %s" %
                  (sbm.name, tagified, latest_tag))
            sbm.set_commit(latest_tag)
