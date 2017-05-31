import argparse
import functools

from git_utils import *

def register_module_args(subparsers):
    parser = subparsers.add_parser("submodule", 
        help="subcommand to deal with submodules in deepin-code-release")

    parser.add_argument("--status", action="store_true",
        help="show submodule current status.")

def run_with_module_args(args):
    if args.subcommand != __name__:
        return

    if args.status:
        status()

def status():
    sbms = git_submodule_list()
    for sbm in sbms:
        _tagify = functools.partial(git_submodule_commit_to_tag, sbm)
        tagify = lambda x: _tagify(x) or x
        current_commit = git_submodule_get_commit(sbm)
        latest_commit = git_submodule_latest_commit(sbm)
        
        print("%s: current commit %s, remote latest commit %s." % 
             (sbm, tagify(current_commit), tagify(latest_commit)))
