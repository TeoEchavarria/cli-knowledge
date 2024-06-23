import argparse
from cli.main import commands_creator
from config.json import yagami

def main():
    parser = argparse.ArgumentParser(description="Task management script")
    subparsers = parser.add_subparsers(dest='command', required=True)

    commands_creator(subparsers, yagami)
    
    args = parser.parse_args()
    print(args._get_args)
    
if __name__ == "__main__":
    main()