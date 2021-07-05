import os, os.path
import yaml
from types import CodeType
from scripts.build import PythonScriptDictionary
import scripts.util as util
import importlib.util
import importlib._bootstrap_external as bse
def to_code_object(table: PythonScriptDictionary):
    return CodeType(table.argcount, table.posonlyargcount, table.kwonlyargcount, table.nlocals, table.stacksize, table.flags, table.code, translate_tuple(table.consts), table.names, table.varnames, table.filename, table.name, table.firstlineno, table.lnotab, table.freevars, table.cellvars)
def translate_tuple(input: tuple):
    output = []
    for element in input:
        if element.__class__ == PythonScriptDictionary:
            output.append(to_code_object(element))
        else:
            output.append(element)
    return tuple(output)
def compile_file(build_dir: str, script_path: str, cache_dir: str):
    output_path = os.path.join(cache_dir, script_path) + "c"
    code_data = None
    with open(os.path.join(build_dir, script_path) + ".yml", "r") as stream:
        try:
            code_data = yaml.load(stream, Loader=yaml.Loader)
            stream.close()
        except yaml.YAMLError as exc:
            print(exc)
    if code_data == None:
        print("Could not read code data; terminating...")
        exit(1)
    code = to_code_object(code_data)
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
    cache_dir = os.path.join(build_dir, "__cache__")
    print("Build directory: {}\nFile to run: {}".format(build_dir, file))
    config_file = open(os.path.join(build_dir, "config.yml"), "r")
    config = yaml.load(config_file, Loader=yaml.Loader)
    config_file.close()
    if config.assets != None:
        print("Copying assets...")
        util.copy_directory(os.path.join(build_dir, config.assets), cache_dir)
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
                output_path = compile_file(build_dir, script_path, cache_dir)
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