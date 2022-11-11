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


LEFT_CUBE = "red"
RIGHT_CUBE = "blue"
GOAL_CUBE = "black"

NORTH, SOUTH, EAST, WEST = list("NSEW")
LEFT = "L"
RIGHT = "R"

def add_grid_line(row, col, lineName, yaw=0):
    include = re.sub("MODEL-NAME", lineName, INCLUDE_LINE_TEMPLATE)

    model = re.sub("MODEL-NAME", lineName, MODEL_LINE_TEMPLATE)
    model = re.sub("MODEL-YAW", str(yaw), model)
    model = re.sub("MODEL-X", str(2 * col), model)
    model = re.sub("MODEL-Y", str(2 * row), model)

    return include, model

def add_box(turn_cube, model_num, block_row, block_col, 
            block_row_adj, block_col_adj):
    box_file = f"{turn_cube}_box"
    box_name = f"{box_file}_{model_num}"

    include = re.sub("MODEL-NAME", box_name, INCLUDE_BOX_TEMPLATE)
    include = re.sub("MODEL-FILE", box_file, include)
    include = re.sub("MODEL-BOX", box_name, include)
    

    model = re.sub("MODEL-NAME", box_name, MODEL_BOX_TEMPLATE)
    model = re.sub("MODEL-YAW", "0", model)
    model = re.sub("MODEL-X", str(block_row + block_row_adj), model)
    model = re.sub("MODEL-Y", str(block_col + block_col_adj), model)
    
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

    ''''''
    for col in range(columns+1):
        for row in [_ * .5 for _ in range(2 * rows)]:
            lineName = f"yellowline_{model_num}"

            include, model = add_grid_line(row, col, lineName, yaw=pi/2)

            includes.append(include)
            models.append(model)

            model_num += 1
            

    rows = text_maze.split("\n")
    rows.reverse()
    text_maze = "\n".join(rows)

    print(text_maze)
    text_maze = re.sub("#", " ", text_maze)
    print()
    print(text_maze)

    rows = text_maze.split("\n")
    rows = [list(_) for _ in rows]

    cur_row = 1
    cur_col = 1
    cur_dir = SOUTH 
    next_dir = SOUTH

    visited = set()

    while rows[cur_row][cur_col] != "E":
        visited.add((cur_row, cur_col))

        print(rows[cur_row][cur_col], cur_dir)

        next_pos = {
            SOUTH : (cur_row + 1, cur_col),
            NORTH : (cur_row - 1, cur_col), 
            EAST  : (cur_row, cur_col + 1), 
            WEST  : (cur_row, cur_col - 1),
        }

        for direction in next_pos:
            checkRow, checkCol = next_pos[direction]
            if rows[checkRow][checkCol] in ".E" and (checkRow, checkCol) not in visited:
                next_row = checkRow
                next_col = checkCol 
                next_dir = direction

        
        LEFT_TURNS =  {
            (NORTH, WEST) : (cur_row - 1, cur_col,  .25,  0),
            (SOUTH, EAST) : (cur_row + 1, cur_col, -.25,  0), 
            (EAST, NORTH) : (cur_row, cur_col + 1,  0, -.25),
            (WEST, SOUTH) : (cur_row, cur_col - 1,  0,  .25)
        }
        RIGHT_TURNS =  {
            (NORTH, EAST) : (cur_row - 1, cur_col,  .25, 0),
            (SOUTH, WEST) : (cur_row + 1, cur_col, -.25, 0), 
            (EAST, SOUTH) : (cur_row, cur_col + 1,  0, -.25),
            (WEST, NORTH) : (cur_row, cur_col - 1,  0,  .25)
        }

        turn = (cur_dir, next_dir)
        if turn in LEFT_TURNS:
            turn_dir = LEFT 
            turn_cube = LEFT_CUBE
            block_row, block_col, block_row_adj, block_col_adj = LEFT_TURNS[turn]
        elif turn in RIGHT_TURNS:
            turn_dir = RIGHT 
            turn_cube = RIGHT_CUBE
            block_row, block_col, block_row_adj, block_col_adj = RIGHT_TURNS[turn]
        elif cur_dir == next_dir:
            turn_dir = block_row = block_col = turn_cube = None
            block_row_adj = block_col_adj = None
        else:
            raise Exception(f"Bad turn: {[cur_dir, next_dir]}")

        if turn_dir != None:
            include, model = add_box(turn_cube, model_num, block_row-1, block_col-1, 
                                    block_row_adj, block_col_adj)
            includes.append(include)
            models.append(model)

            model_num += 1

            rows[block_row][block_col] = turn_dir

        cur_col = next_col
        cur_row = next_row
        cur_dir = next_dir

        print(f"{cur_row} {cur_col} {cur_dir} turn_dir={turn_dir}")


    include, model = add_box(GOAL_CUBE, model_num, 
                            cur_row-1, cur_col-1, 
                            0, -.25)
    includes.append(include)
    models.append(model)
    
    print()
    for row in rows:
        print(''.join(row))

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
    solved_text_maze = solver(text_maze)

    make_world(rows, columns, solved_text_maze)


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
