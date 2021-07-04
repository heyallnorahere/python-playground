from typing import Tuple
from scripts.script_types import *
def get_code_dict(code: CodeType, relative_bytecode_path: str):
    return {
        "argcount": code.co_argcount,
        "cellvars": code.co_cellvars,
        # todo: translate tuples such as consts
        #"consts": code.co_consts,
        "filename": code.co_filename,
        "firstlineno": code.co_firstlineno,
        "flags": code.co_flags,
        "freevars": code.co_freevars,
        "kwonlyargcount": code.co_kwonlyargcount,
        "lnotab": code.co_lnotab,
        "name": code.co_name,
        "names": code.co_names,
        "nlocals": code.co_nlocals,
        "posonlyargcount": code.co_posonlyargcount,
        "stacksize": code.co_stacksize,
        "varnames": code.co_varnames,
        "relative_bytecode_path": relative_bytecode_path
    }
def build(args: list[str]):
    directory_name = os.path.dirname(os.path.realpath(__file__))
    source_directory = directory_name + "/../"
    sources = None
    sources_file = source_directory + "sources.yml"
    if len(args) >= 3:
        sources_file = args[2]
    with open(sources_file, "r") as stream:
        try:
            sources = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    if sources == None:
        print("Could not load sources list; terminating...")
        exit(1)
    for path in sources["files"]:
        print("Compiling %s..." % (path))
        file = open(source_directory + str(path), "r")
        data = compile(file.read(), path, "exec")
        try:
            os.mkdir(directory_name + "/build/" + os.path.dirname(path))
        except FileExistsError: pass
        output = open(directory_name + "/build/" + str(path) + ".bytecode", "wb")
        output.write(data.co_code)
        output.close()
        output = open(directory_name + "/build/" + str(path) + ".yml", "w")
        rep = get_code_dict(data, str(path) + ".bytecode")
        yaml.dump(rep, output)
        output.close()
        file.close()
        output.close()
    print("Output written to: %s" % (directory_name + "/build"))
