def commands_creator(parser, config):
    subparsers = parser.add_subparsers(dest='command', required=True)
    for command in config:
        tal_parser = subparsers.add_parser(command["command"], help = command["description"], aliases=[command["alias"]])
        tal_subparsers = tal_parser.add_subparsers(dest='action', help='task actions')
        for subcommand in command["subcommands"]:
            sub_parser = tal_subparsers.add_parser(subcommand['subcommand'], help=subcommand["description"], aliases=[subcommand["alias"]])
            for attribut in subcommand["attributes"]:
                sub_parser.add_argument(f"--{attribut['name']}", f"-{attribut['alias']}", help=attribut["description"], required=attribut["required"], type=attribut["type"])
