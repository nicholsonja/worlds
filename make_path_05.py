#!/usr/bin/env python

import re
import sys
from math import pi
from random import shuffle
from mazelib.grid import Grid
from mazelib.kruskal import Kruskals
from mazelib.solver import solver
from pathlib import INPUT_TEMPLATE_FILE, OUTPUT_WORLD_FILE, INCLUDE_BOX_TEMPLATE, \
    MODEL_BOX_TEMPLATE, GROUND_MODEL, GROUND_INCLUDE, INCLUDE_LINE_TEMPLATE, MODEL_LINE_TEMPLATE


def add_grid_line(row, col, lineName, yaw=0):
    include = re.sub("MODEL-NAME", lineName, INCLUDE_LINE_TEMPLATE)

    model = re.sub("MODEL-NAME", lineName, MODEL_LINE_TEMPLATE)
    model = re.sub("MODEL-YAW", str(yaw), model)
    model = re.sub("MODEL-X", str(2 * col), model)
    model = re.sub("MODEL-Y", str(2 * row), model)

    return include, model


def get_includes_and_models(rows, columns, text_maze):

    includes = []
    models = []

    model_num = 0
    for row in range(rows+1):
        for col in [_ * .5 for _ in range(2 * columns)]:
            lineName = f"yellowline_{model_num}"

            include, model = add_grid_line(row, col, lineName)

            includes.append(include)
            models.append(model)

            model_num += 1

    for col in range(columns+1):
        for row in [_ * .5 for _ in range(2 * rows)]:
            lineName = f"yellowline_{model_num}"

            include, model = add_grid_line(row, col, lineName, yaw=pi/2)

            includes.append(include)
            models.append(model)

            model_num += 1

    return includes, models


def make_world(rows, columns, text_maze):
    with open(INPUT_TEMPLATE_FILE, "r") as fin:
        template = fin.readlines()

    includes, models = get_includes_and_models(rows, columns, text_maze)

    with open(OUTPUT_WORLD_FILE, "w") as fout:
        for line in template:
            if "<!--MODEL LOCATION-->" in line:
                models = "\n".join(models)
                fout.write(models)
            elif "<!--INCLUDE LOCATION-->" in line:
                includes = "\n".join(includes)
                fout.write(includes)
            else:
                fout.write(line)


def main(rows, columns, cell_width):

    #grid = Grid(rows, columns)

    # Kruskals.on(grid)

    #text_maze = grid.to_string(do_print=False, cell_width=cell_width)

    #solved_text_maze = solver(text_maze)

    # print("HERE")
    # print(solved_text_maze)

    text_maze = ""

    make_world(rows, columns, text_maze)


if __name__ == "__main__":

    cell_width = 2
    if len(sys.argv) == 1:
        rows = 2
        columns = 2
    elif len(sys.argv) == 3:
        rows = int(sys.argv[1])
        columns = int(sys.argv[2])
    else:
        print(f"USAGE: {sys.argv[0]} ROWS COLUMNS")
        exit(0)

    if rows < 2 or columns < 2:
        print("ERROR: Values for ROWS, COLUMNS must all be >= 2")
        exit(0)

    main(rows, columns, cell_width)
