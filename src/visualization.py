import json
import networkx as nx
import matplotlib.pyplot as plt

def visualize_analysis(json_file="analysis/analysis.json"):
    with open(json_file) as f:
        data = json.load(f)

    G = nx.DiGraph()

    # Add nodes
    for py in data.get("python", []):
        for cls in py.get("classes", []):
            G.add_node(cls, color="lightblue")
        for func in py.get("functions", []):
            G.add_node(func, color="lightgreen")

    for bash in data.get("bash", []):
        for func in bash.get("functions", []):
            G.add_node(func, color="orange")
        for cmd in bash.get("commands", []):
            G.add_node(cmd, color="yellow")

    for sql in data.get("sql", []):
        for table in sql.get("tables", []):
            G.add_node(table, color="pink")
        for query in sql.get("queries", []):
            G.add_node(query, color="red")

    # Example edges (extend logic later)
    for sql in data.get("sql", []):
        for query in sql.get("queries", []):
            G.add_edge("Python Function", query)

    pos = nx.spring_layout(G)
    colors = [G.nodes[n].get("color", "gray") for n in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=colors, edge_color="black")
    plt.show()


if __name__ == "__main__":
    visualize_analysis()
