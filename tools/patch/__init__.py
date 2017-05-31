import argparse

def register_module_args(subparsers):
    parser = subparsers.add_parser("patch", 
        help="subcommand to deal with patches in deepin-code-release.")

    parser.add_argument("--list", action="store_true", 
        help="list all patches.")

def run_with_module_args(args):
    if args.subcommand != __name__:
        return

    if args.list:
        list_patches()

def list_patches():
    print("list patches")