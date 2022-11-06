#!/usr/bin/env python

import re
import sys
from math import pi
from pathlib import INCLUDE_TEMPLATE, MODEL_TEMPLATE, INPUT_TEMPLATE_FILE, OUTPUT_WORLD_FILE, INCLUDE_END_TEMPLATE
from mazelib.grid import Grid
from mazelib.kruskal import Kruskals

ROT_SOUTH = 0/2 * pi
ROT_EAST = 1/2 * pi
ROT_NORTH = 2/2 * pi
ROW_WEST = 3/2 * pi


def build_line(name, model_x, model_y, model_yaw, include_template=INCLUDE_TEMPLATE):
    include = re.sub("MODEL-NAME", name, include_template)

    model = re.sub("MODEL-NAME", name, MODEL_TEMPLATE)
    model = re.sub("MODEL-YAW", str(model_yaw), model)
    model = re.sub("MODEL-X", str(model_x), model)
    model = re.sub("MODEL-Y", str(model_y), model)

    return include, model


def get_includes_and_models(rows, columns, text_maze):
    lines = text_maze.split("\n")
    lines.reverse()
    #text_maze = "\n".join(lines)

    # print(text_maze)

    includes = []
    models = []

    model_num = 0
    model_x = -1
    model_yaw = 0

    for row_num, row in enumerate(lines):
        model_y = 0
        for ch_num, ch in enumerate(row):
            print(ch, end="")

            if ch in " RE":

                if ch != 'E' and row[ch_num+1] in " E":
                    model_num += 1
                    if row[ch_num+1] == "E":
                        name = f"purpleline_{model_num}"
                        include_template = INCLUDE_END_TEMPLATE
                    else:
                        name = f"yellowline_{model_num}"
                        include_template = INCLUDE_TEMPLATE

                    model_yaw = ROW_WEST
                    include, model = build_line(
                        name, model_x, model_y, model_yaw, include_template)
                    includes.append(include)
                    models.append(model)

                if lines[row_num+1][ch_num] == " ":
                    model_num += 1
                    name = f"yellowline_{model_num}"

                    model_yaw = ROT_SOUTH
                    include, model = build_line(
                        name, model_x, model_y-1, model_yaw)
                    includes.append(include)
                    models.append(model)

            model_y += 1

        print()
        model_x += 1

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

    grid = Grid(rows, columns)

    Kruskals.on(grid)

    text_maze = grid.to_string(do_print=False, cell_width=cell_width)

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
