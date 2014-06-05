import argument_parser
import commands
import sys

COMMANDS = {
    "login": commands.login,
    "ls": commands.ls,
    "add": commands.add,
    "rm": commands.rm,
    "mv": commands.mv,
    "tag": commands.tag,
    "rmtag": commands.rmtag,
    "search": commands.search,
    "fetch": commands.fetch,
    "edit": commands.edit
}

def main():
    """ Main function """
    parser = argument_parser.make_parser()
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    try:
        COMMANDS[command](**arguments)
    except Exception as error:
        exit(str(error))
