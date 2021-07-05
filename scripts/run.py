from scripts.script_types import *
import importlib.util
import importlib._bootstrap_external as bse
import dis
def compile_file(build_dir: str, script_path: str):
    cache_dir = os.path.join(build_dir, "__cache__")
    output_path = os.path.join(cache_dir, script_path) + "c"
    code_data = None
    with open(os.path.join(build_dir, script_path) + ".yml", "r") as stream:
        try:
            code_data = yaml.load(stream)
            stream.close()
        except yaml.YAMLError as exc:
            print(exc)
    if code_data == None:
        print("Could not read code data; terminating...")
        exit(1)
    code = CodeType(code_data["argcount"], code_data["posonlyargcount"], code_data["kwonlyargcount"], code_data["nlocals"], code_data["stacksize"], code_data["flags"], code_data["code"], code_data["consts"], code_data["names"], code_data["varnames"], code_data["filename"], code_data["name"], code_data["firstlineno"], code_data["lnotab"], code_data["freevars"], code_data["cellvars"])
    pyc_data = bse._code_to_timestamp_pyc(code)
    try:
        os.mkdir(os.path.dirname(output_path))
    except FileExistsError as exc: pass
    output_file = open(output_path, "wb")
    output_file.write(pyc_data)
    output_file.close()
    return output_path
def run(args: list[str]):
    if len(args) < 4:
        print("Usage: {python command} -m scripts run <directory> <file>")
        exit(1)
    build_dir = args[2]
    file = args[3]
    print("Build directory: {}\nFile to run: {}".format(build_dir, file))
    print("Reading code data...")
    pyc_path = None
    for root, dirs, files in os.walk(build_dir):
        for name in files:
            if name.endswith(".py.yml"):
                fullpath = os.path.join(root, name)
                trailing_slash_path = build_dir
                if not build_dir.endswith("/"):
                    trailing_slash_path += "/"
                strings = fullpath.split(trailing_slash_path)
                relative_path = strings[len(strings) - 1] # splits the path, and gets the last section between occurrences of the separator
                script_path = relative_path.split(".yml")[0] # next, gets the relative path of the script before compilation
                output_path = compile_file(build_dir, script_path)
                if file == script_path:
                    pyc_path = os.path.realpath(output_path)
    if pyc_path == None:
        print("Could not find specified entrypoint; aborting...")
        exit(1)
    print("Successfully loaded code!")
    os.chdir(os.path.dirname(pyc_path))
    spec = importlib.util.spec_from_file_location("<module>", pyc_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)