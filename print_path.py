import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from Utils.utlities import transpose_graph, transpose_path

def display_path(path, graph, show_axes=True, show_title=True, file_name=None):
    """
    path:  list of (x, y) tuples in visiting order
    graph: dict {square: neighbors}
           (we only need the set of vertices)
    """

    graph = transpose_graph(graph)
    path = transpose_path(path)

    nodes = set(graph.keys())

    max_x = max(x for x, y in nodes)
    max_y = max(y for x, y in nodes)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Background color (holes will match this)
    background_color = "#ffffff"
    fig.patch.set_facecolor(background_color)

    ax.set_xlim(-0.5, max_x + 0.5)
    ax.set_ylim(-0.5, max_y + 0.5)
    ax.set_aspect('equal')

    # Draw checkerboard only on valid squares
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if (x, y) in nodes:
                color = "#efd1a1" if (x + y) % 2 == 0 else "#211102"
            else:
                color = background_color  # hole
            ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color=color))

    # Draw labels and circles
    for i, (x,y) in enumerate(path):
        label = str(i + 1)

        if i == 0 or i == len(path) - 1:  
            # Start or end → draw circle
            circle = Circle((x, y), radius=0.45, fill=False, color='white', linewidth=2)
            ax.add_patch(circle)

        if (x + y) % 2 == 0:
            # Light square → dark text
            ax.text(x, y, label, ha='center', va='center',
                    fontsize=22, color='black')
        else:
            # Dark square → light text  
            ax.text(x, y, label, ha='center', va='center',
                    fontsize=22, color='lightgray')

    ax.invert_yaxis()

    if show_axes:
        ax.set_xticks(range(max_x + 1))
        ax.set_yticks(range(max_y + 1))
        ax.grid(False)
    else:
        ax.axis('off')

    if show_title:
        ax.set_title("Labeled Knight Hamiltonian Path")

    plt.show()
