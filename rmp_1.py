from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from PIL import ImageDraw
import random
import cv2
import networkx as nx


def create_grid(grid_width, num_obstacles):
    grid = np.zeros((grid_width, grid_width))
    obst = create_obstacles(num_obstacles, grid_width)
    for idx, o in enumerate(obst):
        s = obst[idx].shape[0]
        rnd_pos_y = np.random.randint(0, grid_width - int(grid_width // 10))
        rnd_pos_x = np.random.randint(0, grid_width - int(grid_width // 10))

        for i in range(s):
            grid[rnd_pos_y + i][rnd_pos_x:rnd_pos_x + s] = o[i]
    return grid


def create_obstacles(num_obstacles, grid_width):
    obst = []
    for idx in range(num_obstacles):
        rand_size = np.random.randint(int(grid_width // 20), int(grid_width // 10))
        obst.append(np.ones((rand_size, rand_size)))
    return obst


def plot_grid(obst_grid, c_grid, robot_occupancy_grid, vert_grid, g):
    f, axarr = plt.subplots(1, 4, figsize=(25,10))
    axarr[0].imshow(np.add(obst_grid, robot_occupancy_grid))
    axarr[0].invert_yaxis()
    axarr[0].set_title("obstacles & robot arm")
    axarr[1].imshow(c_grid)
    axarr[1].invert_yaxis()
    axarr[1].set_title("c_obstacles")
    axarr[2].imshow(vert_grid)
    axarr[2].invert_yaxis()
    axarr[2].set_title("polygon obstacles and corner detection")
    nx.draw(g, nx.get_node_attributes(g, 'pos'))
    axarr[3].plot()
    axarr[3].set_title("graph of polygon model")
    axarr[3].grid(True)
    axarr[3].set_xlim(0, vert_grid.shape[0])
    axarr[3].set_ylim(0, vert_grid.shape[1])
    plt.show()


def create_robot(theta_1, theta_2, grid_size, obst_grid):
    length_1 = 80
    length_2 = 30
    robot_occupancy_grid = np.zeros((grid_size, grid_size))
    c_grid = np.zeros((360, 360))

    for i in range(1, theta_1):
        for l in range(length_1):
            x_1 = int(l * np.cos(i / 360 * np.pi) + grid_size / 2)
            y_1 = int(l * np.sin(i / 360 * np.pi))
            robot_occupancy_grid[y_1][x_1] = 1
            if obst_grid[y_1][x_1] == 1:
                c_grid[:, i] = 1

    for k in range(theta_1):
        x_1 = int(length_1 * np.cos(k / 360 * np.pi) + grid_size / 2)
        y_1 = int(length_1 * np.sin(k / 360 * np.pi))
        for i in range(1, theta_2):
            for l in range(length_2):
                x_2 = int(l * np.cos(i / 360 * np.pi)) + x_1
                y_2 = int(l * np.sin(i / 360 * np.pi)) + y_1
                if x_2 < grid_size and y_2 < grid_size:
                    robot_occupancy_grid[y_2][x_2] = .5
                    if obst_grid[y_2][x_2] == 1:
                        c_grid[i][k] = 1

    return c_grid, robot_occupancy_grid


def create_polygons(grid_size, nm_polygons):
    img = Image.fromarray(np.zeros((grid_size, grid_size)))
    draw = ImageDraw.Draw(img)
    verts = []
    for i in range(nm_polygons):
        mid_x = np.random.randint(1, grid_size - grid_size // 12)
        mid_y = np.random.randint(1, grid_size - grid_size // 12)
        vert = list(zip(np.add([0, 80, 50, 150, 10], mid_x), np.add([0, 50, 140, 30, 100], mid_y)))
        random.shuffle(vert)
        verts.append(vert)
        draw.polygon(vert, fill="wheat")
    return np.array(img / np.max(img)), verts


def corners(vert_grid):
    corners = cv2.goodFeaturesToTrack(vert_grid, 100, 0.18, 10)
    print(f"detected {corners.shape[0]} corners")
    img = Image.fromarray(vert_grid)
    draw = ImageDraw.Draw(img)
    r = 5

    for c in range(corners[:, 0, :].shape[0]):
        x = int(corners[:, 0, :][c][0])
        y = int(corners[:, 0, :][c][1])
        vert_grid[x, y] += 1
        draw.ellipse([(x - r, y - r), (x + r, y + r)])

    return corners[:, 0, :], vert_grid, np.array(img) / np.max(np.array(img))


def draw_graph(corners, nm_corners, nm_polygons):
    g = nx.Graph()
    g.add_nodes_from(range(corners.shape[0]))
    l = 0
    for i in range(corners.shape[0]):
        if i % nm_polygons // nm_corners == 0:
            l += 1
        for j in range(corners.shape[0]):
            if j != i and j not in [k for k in range(5 * (l - 1), 5 * l)]:
                g.add_edge(i, j)

    for i in range(corners.shape[0]):
        g.add_node(i, pos=corners[i])

    return g


if __name__ == "__main__":
    grid_size = 500
    nm_polygons = 3
    obst_grid = create_grid(grid_size, 20)
    vert_grid, verts = create_polygons(grid_size, nm_polygons)
    corners, vert_grid, vert_grid_corners = corners(vert_grid)

    c_grid, robot_occupancy_grid = create_robot(360, 360, grid_size, obst_grid)
    g = draw_graph(corners, corners.shape[0], nm_polygons)
    plot_grid(obst_grid, c_grid, robot_occupancy_grid, vert_grid_corners, g)
