import argparse

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
    print("status")