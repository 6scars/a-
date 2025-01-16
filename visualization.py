import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap, BoundaryNorm
from a_star import read_grid, a_star_with_animation
import matplotlib

matplotlib.use('TkAgg')
import numpy as np


def colors(grid):
    colors = [
        (1, 1, 1),  # 0 tło
        (0, 1, 1),  # 1 start
        (1, 1, 0),  # 2 meta


        (0, 0, 0.7),    # 3 sąsiedzi obok current node
        (1, 1, 0),      # 4 droga od startu do mety
        (0, 0, 0.1),    # 5 przeszkody
        (1, 0, 0)       #7 current note jako czerwony

    ]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm([0, 1, 2, 3, 4, 5, 7], cmap.N)  # Przypisanie wartości do kolorów
    return cmap, norm

# dostosowanie grafu, przesunięcie w lewo pozycji głównie
def personalize_the_graph(ax, grid):
    ax.set_title("Algorytm A* - Animacja kratka po kratce")
    # Przesunięcie etykiet osi

    # Pozycja "0" lekko przesunięta w lewo
    ax.set_xticks(np.arange(-0.5, grid.shape[1], 1))
    ax.set_yticks(np.arange(-0.5, grid.shape[0], 1))
    # Dostosowanie numeracji
    ax.set_xticklabels(np.arange(0, grid.shape[1] + 1))
    ax.set_yticklabels(np.arange(0, grid.shape[0] + 1))

    # Dostosowanie widocznych krawędzi
    ax.grid(which="both", color="gray", linestyle="-", linewidth=0.5)
    ax.set_xlim(-0.5, grid.shape[1] - 0.5)  # Dopasowanie granic osi
    ax.set_ylim(grid.shape[0] - 0.5, -0.5)

    return ax


def visualize(grid, anim_frames):
    grid = np.array(grid)

    fig, ax = plt.subplots()
    ax = personalize_the_graph(ax, grid)

    # Inicjalizacja siatki wizualizacji
    colors_and_indexes = colors(grid)
    im = ax.imshow(grid, cmap=colors_and_indexes[0], norm=colors_and_indexes[1], interpolation='nearest')

    def update(frame_idx):
        im.set_data(anim_frames[frame_idx])
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(anim_frames), interval=1, repeat=False, blit=True)
    plt.show()


if __name__ == "__main__":
    file_path = "C:/Users/1/Desktop/AstarPB/grid.txt"
    grid = read_grid(file_path)
    start = (len(grid) - 1, 0)
    goal = (0, len(grid[0]) - 1)


    # Dane do animacji
    anim_frames = []
    visual_grid = [[cell for cell in row] for row in grid]
    visual_grid[start[0]][start[1]] = 1  # Start
    visual_grid[goal[0]][goal[1]] = 2  # Meta

    # Uruchom algorytm i animację
    path = a_star_with_animation(grid, start, goal, anim_frames)
    if path:
        print("Znaleziono ścieżkę:", path[0])
    else:
        print("Nie znaleziono ścieżki")

    # Wizualizacja
    visualize(visual_grid, anim_frames)
