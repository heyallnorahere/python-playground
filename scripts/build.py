from scripts.script_types import *
class CodeRepresentation:
    def __init__(self, code: types.CodeType, relative_bytecode_path: str):
        self.argcount = code.co_argcount
        self.cellvars = code.co_cellvars
        #self.consts = code.co_consts
        self.filename = code.co_filename
        self.firstlineno = code.co_firstlineno
        self.flags = code.co_flags
        self.freevars = code.co_freevars
        self.kwonlyargcount = code.co_kwonlyargcount
        self.lnotab = code.co_lnotab
        self.name = code.co_name
        self.nlocals = code.co_nlocals
        self.posonlyargcount = code.co_posonlyargcount
        self.stacksize = code.co_stacksize
        self.varnames = code.co_varnames
        self.relative_bytecode_path = relative_bytecode_path
def build():
    directory_name = os.path.dirname(os.path.realpath(__file__))
    source_directory = directory_name + "/../"
    sources = None
    with open(source_directory + "sources.yml", "r") as stream:
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
        rep = CodeRepresentation(data, str(path) + ".bytecode")
        yaml.dump(rep, output)
        output.close()
        file.close()
        output.close()
    print("Output written to: %s" % (directory_name + "/build"))
