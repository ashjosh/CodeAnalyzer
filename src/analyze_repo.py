import json
from tree_sitter import Language, Parser
import os

LIB_PATH = "build/my-languages.dll"  # Windows will produce a DLL

if not os.path.exists(LIB_PATH):
    Language.build_library(
        LIB_PATH,
        [
            "vendor/tree-sitter-python",
            "vendor/tree-sitter-bash",
            "vendor/tree-sitter-sql",
        ]
    )
PY_LANGUAGE = Language(LIB_PATH, "python")
BASH_LANGUAGE = Language(LIB_PATH, "bash")
SQL_LANGUAGE = Language(LIB_PATH, "sql")

py_parser = Parser()
py_parser.set_language(PY_LANGUAGE)

bash_parser = Parser()
bash_parser.set_language(BASH_LANGUAGE)

sql_parser = Parser()
sql_parser.set_language(SQL_LANGUAGE)

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

def parse_sql(code: bytes):
    tree = sql_parser.parse(code)
    root = tree.root_node
    tables, queries = [], []
    for child in root.children:
        if child.type == "create_table_statement":
            tables.append(code[child.start_byte:child.end_byte].decode())
        elif child.type in ["select_statement", "insert_statement", "update_statement"]:
            queries.append(code[child.start_byte:child.end_byte].decode())
    return {"tables": tables, "queries": queries}

def analyze_repo(path):
    results = {"python": [], "bash": [], "sql": []}
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                code = open(full_path, "rb").read()
            except Exception:
                continue

            if file.endswith(".py"):
                results["python"].append(parse_python(code))
            elif file.endswith(".sh"):
                results["bash"].append(parse_bash(code))
            elif file.endswith(".sql"):
                results["sql"].append(parse_sql(code))
    return results

if __name__ == "__main__":
    repo_path = "repo"  # use your already-cloned repo folder
    analysis = analyze_repo(repo_path)

    os.makedirs("analysis", exist_ok=True)
    with open("analysis/analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)

    print("✅ Analysis complete! Results saved to analysis/analysis.json")
