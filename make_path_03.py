#!/usr/bin/env python

import re
from sys import argv, exit
from mazelib.grid import Grid
from mazelib.kruskal import Kruskals


INPUT_TEMPLATE_FILE = "path-template.xml"
OUTPUT_WORLD_FILE = "path_world.xml"


#
# MODEL_TEMPLATE = """
#      <model name='MODEL-NAME'>
#        <pose>MODEL-X MODEL-Y 0.25 0 -0 0</pose>
#        <scale>1 1 1</scale>
#        <link name='link_0'>
#          <pose>MODEL-X MODEL-Y 0.25 0 -0 0</pose>
#          <velocity>0 0 0 0 -0 0</velocity>
#          <acceleration>0 -0 0 0 -0 0</acceleration>
#          <wrench>0 -0 0 0 -0 0</wrench>
#        </link>
#      </model>
# """

MODEL_TEMPLATE = """
      <model name='MODEL-NAME'>
        <scale>1 1 1</scale>
        <pose>MODEL-X MODEL-Y 0 0 -0 0</pose>
        <velocity>0 0 0 0 -0 0</velocity>
        <acceleration>0 -0 0 0 -0 0</acceleration>
        <wrench>0 -0 0 0 -0 0</wrench>
      </model>
"""

INCLUDE_TEMPLATE = """
    <model name='MODEL-NAME'>
      <static>1</static>
      <include>
        <uri>model:///home/user/worlds/models/line</uri>
	  </include>
    </model>
"""


def get_includes_and_models(rows, columns, text_maze):
    lines = text_maze.split("\n")
    lines.reverse()
    #text_maze = "\n".join(lines)

    # print(text_maze)

    includes = []
    models = []

    model_num = 0
    model_x = -1
    for row in lines:
        model_y = -1
        for ch in row:
            print(ch, end="")

            if ch == " ":
                name = f"yellowline_{model_num}"

                include = re.sub("MODEL-NAME", name, INCLUDE_TEMPLATE)
                includes.append(include)

                model = re.sub("MODEL-NAME", name, MODEL_TEMPLATE)
                model = re.sub("MODEL-X", str(model_x), model)
                model = re.sub("MODEL-Y", str(model_y), model)
                models.append(model)

            model_y += 1
            model_num += 1
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
    if len(argv) == 1:
        rows = 1
        columns = 1
    elif len(argv) == 3:
        rows = int(argv[1])
        columns = int(argv[2])
    else:
        print(f"USAGE: {argv[0]} ROWS COLUMNS")
        exit(0)

    if rows < 2 or columns < 2:
        print("ERROR: Values for ROWS, COLUMNS, and CELL_SIZE must all be >= 2")
        exit(0)

    main(rows, columns, cell_width)
