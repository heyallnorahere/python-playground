from scripts.script_types import *
class CodeRepresentationTable:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
def translate_tuple(input: tuple):
    output = []
    for element in input:
        if element.__class__ == CodeType:
            output.append(get_code_dict(element))
        else:
            output.append(element)
    return tuple(output)
def get_code_dict(code: CodeType):
    return CodeRepresentationTable(
        argcount=code.co_argcount,
        cellvars=code.co_cellvars,
        code=code.co_code,
        consts=translate_tuple(code.co_consts),
        filename=code.co_filename,
        firstlineno=code.co_firstlineno,
        flags=code.co_flags,
        freevars=code.co_freevars,
        kwonlyargcount=code.co_kwonlyargcount,
        lnotab=code.co_lnotab,
        name=code.co_name,
        names=code.co_names,
        nlocals=code.co_nlocals,
        posonlyargcount=code.co_posonlyargcount,
        stacksize=code.co_stacksize,
        varnames=code.co_varnames
    )
def build(args: list[str]):
    sources = None
    sources_file = "./sources.yml"
    if len(args) >= 3:
        sources_file = args[2]
    with open(sources_file, "r") as stream:
        try:
            sources = yaml.safe_load(stream)
            stream.close()
        except yaml.YAMLError as exc:
            print(exc)
    if sources == None:
        print("Could not load sources list; terminating...")
        exit(1)
    source_directory = os.path.realpath(str(sources["directory"]))
    for path in sources["files"]:
        print("Compiling %s..." % (path))
        file = open(os.path.join(source_directory, str(path)), "r")
        data = compile(file.read(), path, "exec")
        try:
            os.mkdir(os.path.join(source_directory, "build", os.path.dirname(path)))
        except FileExistsError: pass
        output = open(os.path.join(source_directory, "build/", str(path)) + ".yml", "w")
        rep = get_code_dict(data)
        yaml.dump(rep, output)
        output.close()
        file.close()
        output.close()
    print("Output written to: {}".format(os.path.join(source_directory, "build")))