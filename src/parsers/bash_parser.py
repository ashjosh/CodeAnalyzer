from tree_sitter import Parser
import tree_sitter_bash as tsbash

bash_parser = Parser()
bash_parser.set_language(tsbash.language())

def parse_bash(code: bytes):
    tree = bash_parser.parse(code)
    root = tree.root_node
    functions, commands = [], []
    for child in root.children:
        if child.type == "function_definition":
            functions.append(code[child.start_byte:child.end_byte].decode())
        elif child.type == "command":
            commands.append(code[child.start_byte:child.end_byte].decode())
    return {"functions": functions, "commands": commands}
