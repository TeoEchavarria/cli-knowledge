def commands_creator(subparsers, config):
    for command in config:
        parser = subparsers.add_parser(command["command"], help = command["description"], aliases=[command["alias"]])
        subparsers = parser.add_subparsers(dest='action', help='task actions')
        for subcommand in command["subcommands"]:
            sub_parser = subparsers.add_parser(subcommand['subcommand'], help=subcommand["description"], aliases=[subcommand["alias"]])
            for attribut in subcommand["attributes"]:
                sub_parser.add_argument(f"--{attribut['alias']}", f"-{attribut['name']}", help=attribut["description"], required=attribut["required"], type=attribut["type"])
