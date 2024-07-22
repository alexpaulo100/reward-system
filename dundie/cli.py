import argparse
from dundie.core import load

def main():
    parser = argparse.ArgumentParser(
        description="Dunder Miifflin Rewards CLI",
        epilog="Enjoy and use with cautious.",
    )
    parser.add_argument(
        "subcommand",
        type=str,
        help="The subcommand to run",
        choices=("load", "show", "send"),
        default='help'
    )
    parser.add_argument(
        "filepath",
        type=str,
        help="File path to load",
        default='none'
    )
    args = parser.parse_args()

    print(*globals()[args.subcommand](args.filepath))
          