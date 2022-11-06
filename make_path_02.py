#!/usr/bin/env python

import re
from pathlib import *
from sys import argv
from math import pi


def get_includes_and_models(num_cells):

    includes = []
    models = []

    model_num = 0
    model_y = 0
    model_x = .5

    for side in range(4):
        if side == 0:
            model_y_inc = 0
            model_x_inc = 1
            model_yaw = pi/2
        elif side == 1:
            model_y += .5
            model_x -= .5
            model_y_inc = 1
            model_x_inc = 0
            model_yaw = 0
        elif side == 2:
            model_y -= .5
            model_x -= .5
            model_y_inc = 0
            model_x_inc = -1
            model_yaw = pi/2
        else:
            model_y -= .5
            model_x += .5
            model_y_inc = -1
            model_x_inc = 0
            model_yaw = 0

        for cell in range(num_cells):

            name = f"yellowline_{model_num}"

            include = re.sub("MODEL-NAME", name, INCLUDE_TEMPLATE)
            includes.append(include)

            model = re.sub("MODEL-NAME", name, MODEL_TEMPLATE)
            model = re.sub("MODEL-YAW", str(model_yaw), model)
            model = re.sub("MODEL-X", str(model_x), model)
            model = re.sub("MODEL-Y", str(model_y), model)
            models.append(model)

            model_num += 1
            model_x += model_x_inc
            model_y += model_y_inc

    return includes, models


def make_world(num_cells):
    with open(INPUT_TEMPLATE_FILE, "r") as fin:
        template = fin.readlines()

    includes, models = get_includes_and_models(num_cells)

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


def main(num_cells):
    make_world(num_cells)


if __name__ == "__main__":
    if len(argv) == 1:
        num_cells = 3
    elif len(argv) == 2:
        num_cells = int(argv[1])
    else:
        print(f"USAGE: {argv[0]} NUM_CELLS")
        exit(0)

    if num_cells < 1:
        print("ERROR: Values for num_cells = 3 must be >= 1")
        exit(0)

    main(num_cells)
