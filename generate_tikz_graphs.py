import sys

adj_list = {(0, 0): [(0, 1)],
 (0, 1): [(0, 0), (0, 2), (1, 1)],
 (0, 2): [(0, 1), (0, 3), (1, 2)],
 (0, 3): [(0, 2), (1, 3)],
 (0, 5): [(1, 5)],
 (1, 1): [(0, 1), (1, 2)],
 (1, 2): [(0, 2), (1, 1)],
 (1, 3): [(0, 3), (1, 4)],
 (1, 4): [(1, 3), (1, 5)],
 (1, 5): [(0, 5), (1, 4), (2, 5)],
 (2, 0): [(3, 0)],
 (2, 3): [(2, 4), (3, 3)],
 (2, 4): [(2, 3), (2, 5), (3, 4)],
 (2, 5): [(1, 5), (2, 4), (3, 5)],
 (3, 0): [(2, 0), (3, 1)],
 (3, 1): [(3, 0), (3, 2), (4, 1)],
 (3, 2): [(3, 1), (3, 3), (4, 2)],
 (3, 3): [(2, 3), (3, 2), (3, 4), (4, 3)],
 (3, 4): [(2, 4), (3, 3), (3, 5), (4, 4)],
 (3, 5): [(2, 5), (3, 4), (4, 5)],
 (4, 0): [(4, 1), (5, 0)],
 (4, 1): [(3, 1), (4, 0), (4, 2), (5, 1)],
 (4, 2): [(3, 2), (4, 1), (4, 3), (5, 2)],
 (4, 3): [(3, 3), (4, 2), (4, 4)],
 (4, 4): [(3, 4), (4, 3), (4, 5)],
 (4, 5): [(3, 5), (4, 4), (5, 5)],
 (5, 0): [(4, 0)],
 (5, 1): [(4, 1), (5, 2)],
 (5, 2): [(4, 2), (5, 1)],
 (5, 5): [(4, 5)]}

def generate_tikz(adj_list):
    output = []
    output.append("\\documentclass[border=10pt]{standalone}")
    output.append("\\usepackage{tikz}")
    output.append("")
    output.append("\\begin{document}")
    # invert y-axis so (0,0) at top-left like typical board drawings
    output.append("\\begin{tikzpicture}[scale=1.0, yscale=-1, every node/.style={circle, fill=black, inner sep=1.5pt}]")
    output.append("")
    output.append("  % --- Vertices ---")
    
    # Track defined nodes to avoid duplicates and define them all first
    nodes = set(adj_list.keys())
    for (x, y) in sorted(nodes):
        node_name = f"node_{x}_{y}"
        output.append(f"  \\node ({node_name}) at ({x},{y}) {{}};")
    
    output.append("")
    output.append("  % --- Edges ---")
    
    # Use a set to store edges to avoid duplicates (undirected graph)
    drawn_edges = set()

    for (u_x, u_y), neighbors in adj_list.items():
        node_u = f"node_{u_x}_{u_y}"
        for (v_x, v_y) in neighbors:
            node_v = f"node_{v_x}_{v_y}"
            # Sort node names to ensure consistent representation of an edge (u, v) and (v, u)
            edge_repr = tuple(sorted((node_u, node_v)))
            if edge_repr not in drawn_edges:
                output.append(f"  \\draw ({node_u}) -- ({node_v});")
                drawn_edges.add(edge_repr)

    output.append("")
    output.append("\\end{tikzpicture}")
    output.append("\\end{document}")
    return "\n".join(output)

if __name__ == "__main__":
    print(generate_tikz(adj_list))

