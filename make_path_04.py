#!/usr/bin/env python

import re
from random import shuffle
from pathlib import INPUT_TEMPLATE_FILE, OUTPUT_WORLD_FILE, INCLUDE_BOX_TEMPLATE, \
    MODEL_BOX_TEMPLATE, GROUND_MODEL, GROUND_INCLUDE


def get_includes_and_models(boxes):

    includes = []
    models = []

    model_x = 4
    model_y = -4

    for box in boxes:
        include = re.sub("MODEL-NAME", box, INCLUDE_BOX_TEMPLATE)
        include = re.sub("MODEL-BOX", box, include)
        includes.append(include)

        model = re.sub("MODEL-NAME", box, MODEL_BOX_TEMPLATE)
        model = re.sub("MODEL-YAW", "0", model)
        model = re.sub("MODEL-X", str(model_x), model)
        model = re.sub("MODEL-Y", str(model_y), model)
        models.append(model)

        model_y += 2

    return includes, models


def make_world(boxes):
    with open(INPUT_TEMPLATE_FILE, "r") as fin:
        template = fin.readlines()

    includes, models = get_includes_and_models(boxes)

    with open(OUTPUT_WORLD_FILE, "w") as fout:
        for line in template:
            if "<!--GROUND MODEL-->" in line:
                fout.write(GROUND_MODEL)
            if "<!--MODEL LOCATION-->" in line:
                models = "\n".join(models)
                fout.write(models)
            elif "<!--INCLUDE LOCATION-->" in line:
                fout.write(GROUND_INCLUDE)
                includes = "\n".join(includes)
                fout.write(includes)
            else:
                fout.write(line)


def main():
    boxes = "black_box blue_box green_box orange_box red_box".split()
    shuffle(boxes)

    make_world(boxes)


if __name__ == "__main__":
    main()
