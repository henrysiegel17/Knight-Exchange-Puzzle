import matplotlib.pyplot as plt
import matplotlib.patches as patches

def display_board(board, max_x, max_y):

    fig, ax = plt.subplots(figsize=(8, 8))

    background_color = "#ffffff"
    fig.patch.set_facecolor(background_color)

    ax.set_xlim(-0.5, max_x + 0.5)
    ax.set_ylim(-0.5, max_y + 0.5)
    ax.set_aspect('equal')

    # Draw checkerboard only on valid squares
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if x < len(board) and y < len(board[0]) and board[y][x] == 1:
                color = "#efd1a1" if (x + y) % 2 == 0 else "#211102"
            else:
                color = background_color
            ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color=color))
    # --------------------------------------------------------------
 # Add black outlines to specific squares
    """special_squares = {
        "A": (9, 7),
        "B": (10, 7),
        "C": (10, 6),
        "D": (10, 8)
    }

    for label, (sx, sy) in special_squares.items():
        # Outline
        ax.add_patch(
            patches.Rectangle(
                (sx - 0.5, sy - 0.5),
                1, 1,
                linewidth=3,
                edgecolor='black',
                facecolor='none'
            )
        )
        # Label at center of square
        ax.text(
            sx, sy, label,
            ha='center', va='center',
            fontsize=18,
            fontweight='bold',
            color='black'
        )
    # --------------------------------------------------------------
    ax.text(
            8, 7, "X",
            ha='center', va='center',
            fontsize=18,
            fontweight='bold',
            color='white'
        )"""
    

    ax.invert_yaxis()
    ax.axis('off')

    plt.show()
