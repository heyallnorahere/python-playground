from scripts import *
import sys
if len(sys.argv) < 2:
    print("No command specified; aborting...")
    exit(1)
commands = {
    "build": build,
    "run": run
}
try:
    commands[sys.argv[1]](sys.argv)
except KeyError as exc:
    print("Command not found! (Specified command: {})".format(exc))
    exit(1)
