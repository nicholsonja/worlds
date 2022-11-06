#!/usr/bin/env python

import re
import sys
from pathlib import INCLUDE_TEMPLATE, MODEL_TEMPLATE, INPUT_TEMPLATE_FILE, OUTPUT_WORLD_FILE


def get_includes_and_models(num_cells):

    includes = []
    models = []

    model_num = 0
    model_y = 0
    model_x = 0
    for cell in range(num_cells):

        name = f"yellowline_{model_num}"

        include = re.sub("MODEL-NAME", name, INCLUDE_TEMPLATE)
        includes.append(include)

        model = re.sub("MODEL-NAME", name, MODEL_TEMPLATE)
        model = re.sub("MODEL-YAW", str(0), model)
        model = re.sub("MODEL-X", str(model_x), model)
        model = re.sub("MODEL-Y", str(model_y), model)
        models.append(model)

        model_num += 1
        model_x += 1

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
    if len(sys.argv) == 1:
        num_cells = 3
    elif len(sys.argv) == 2:
        num_cells = int(sys.argv[1])
    else:
        print(f"USAGE: {sys.argv[0]} NUM_CELLS")
        sys.exit(0)

    if num_cells < 1:
        print("ERROR: Values for num_cells = 3 must be >= 1")
        sys.exit(0)

    main(num_cells)
