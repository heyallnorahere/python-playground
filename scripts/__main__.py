import scripts
import sys
if len(sys.argv) < 2:
    print("No command specified; aborting...")
    exit(1)
def build():
    scripts.build()
commands = {
    "build": build
}
try:
    commands[sys.argv[1]]()
except KeyError as exc:
    print("Command not found! Sorry :/ (Specified command: {})".format(exc))
    exit(1)