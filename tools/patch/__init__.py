'''
patch
'''

import argparse

def register_module_args(subparsers):
    '''
    register_module_args
    '''
    parser = subparsers.add_parser("patch",
                                   help="subcommand to deal with patches in deepin-code-release.")

    parser.add_argument("--list", action="store_true",
                        help="list all patches.")

def run_with_module_args(args):
    '''
    run_with_module_args
    '''
    if args.subcommand != __name__:
        return

    if args.list:
        list_patches()

def list_patches():
    '''
    list_patches
    '''
    print("list patches")
