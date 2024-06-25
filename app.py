import argparse
from cli.main import commands_creator
from config.json import yagami
from importlib import import_module
from utils.argparse import translate_args
from utils.files import initial_markdown_to_list_dict

def main():
    parser = argparse.ArgumentParser(description="Task management script")
    commands_creator(parser, yagami)
    
    args = translate_args(parser.parse_args())
    
    module = import_module(f'cli.actions.{args["action"]}_{args["command"]}')
    function = getattr(module, "run")
    function(args)
    
if __name__ == "__main__":
    initial_markdown_to_list_dict()