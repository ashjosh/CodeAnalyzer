from tree_sitter import Parser
import tree_sitter_python as tspython

py_parser = Parser()
py_parser.set_language(tspython.language())

def parse_python(code: bytes):
    tree = py_parser.parse(code)
    root = tree.root_node
    classes, functions = [], []
    for child in root.children:
        if child.type == "class_definition":
            classes.append(code[child.start_byte:child.end_byte].decode())
        elif child.type == "function_definition":
            functions.append(code[child.start_byte:child.end_byte].decode())
    return {"classes": classes, "functions": functions}
