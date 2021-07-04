from scripts.script_types import *
def run(args: list[str]):
    if len(args) < 4:
        print("Usage: {python command} -m scripts run <directory> <file>")
        exit(1)
    build_dir = args[2]
    file = args[3]
    if not build_dir.endswith("/"):
        print("Directory does not have a trailing slash; adding one")
        build_dir += "/"
    print("Build directory: {}\nFile to run: {}".format(build_dir, file))
    print("Reading code data...")
    code_data = None
    with open(build_dir + file + ".yml", "r") as stream:
        try:
            code_data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    if code_data == None:
        print("Could not read code data; terminating...")
        exit(1)
    bytecode_file = open(build_dir + code_data["relative_bytecode_path"], "rb")
    bytecode = bytecode_file.read()
    bytecode_file.close()
    consts = tuple()
    code = CodeType(code_data["argcount"], code_data["posonlyargcount"], code_data["kwonlyargcount"], code_data["nlocals"], code_data["stacksize"], code_data["flags"], bytecode, consts, code_data["names"], code_data["varnames"], code_data["filename"], code_data["name"], code_data["firstlineno"], code_data["lnotab"], code_data["freevars"], code_data["cellvars"])
    print("Successfully loaded code!")
    exec(code)