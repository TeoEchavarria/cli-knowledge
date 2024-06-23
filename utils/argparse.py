from config.json import yagami
def translate_args(args):
    aliases_command = {command['alias']: command['command'] for command in yagami}
    aliases_subcommands = {command["command"] : { subcommand["alias"]:subcommand["subcommand"]  for subcommand in command["subcommands"]} for command in yagami}
    aliases_attributes = {command["command"] : { subcommand["subcommand"]:{ attribute["alias"]:attribute["name"] for attribute in subcommand["attributes"]}  for subcommand in command["subcommands"]} for command in yagami}
    
    args = vars(args)
    
    if len(args["command"]) == 1:
        args["command"] = aliases_command[args["command"]]
    if len(args["action"]) == 1:
        args["action"] = aliases_subcommands[args["command"]][args["action"]]
    for key, value in list(args.items()):
        if key not in ["command", "action"] and len(key) <= 2:
            args[aliases_attributes[args["command"]][args["action"]][key]] = value
            args.pop(key)
    
    return args