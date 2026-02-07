from tree_sitter import Parser
import tree_sitter_sql as tssql

sql_parser = Parser()
sql_parser.set_language(tssql.language())

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
