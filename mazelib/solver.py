#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 15:56:31 2022

@author: nicholsonja
"""

def generate_path(maze, previous, source, end):
    # make a path of nodes from end to robot
    current = end
    while current != source:
        row = current[0]
        col = current[1]
        if maze[row][col] != 'E':
            maze[row][col] = "."
        current = previous[current]
       
def solve(maze, source_col, source_row, exit_col, exit_row):
    distance = {}
    previous = {}
    unvisited = set()
    
    source = (source_row, source_col)
    end = (exit_row, exit_col)
    
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] != '#':
                node = (row, col)
                
                distance[node] = 99999999
                previous[node] = None
                unvisited.add(node)
    
    distance[source] = 0
    
    while len(unvisited) > 0:
        u = None
        minDist = 99999999
        for node in distance:
            if node in unvisited:
                d = distance[node]
                if d < minDist:
                    minDist = d
                    u = node
        #print("source =", source)
        #print("u =", u)
        #break
        
        unvisited.remove(u)
        #print("unvisited =", sorted(unvisited))
        
    
        neighbors = [
            (u[0] + 1, u[1]),
            (u[0] - 1, u[1]),
            (u[0], u[1] + 1),
            (u[0], u[1] - 1),
            ]
        
        for neighbor in neighbors:
            if neighbor in unvisited:
                alt = distance[u] + 1
                if alt < distance[neighbor]:
                    distance[neighbor] = alt
                    previous[neighbor] = u
          
    generate_path(maze, previous, source, end)

def process_maze(data):
    maze = []
    data = data.split("\n")
    for line in data:
        line = line.rstrip()
        line = [ch for ch in line]
        maze.append(line)  
    return maze

def solver(text_maze):
    maze = process_maze(text_maze)
 
    source_col = 1
    source_row = len(maze) - 2
    
    exit_col = len(maze[0]) - 1
    exit_row = 1
    
    solve(maze, source_col, source_row, exit_col, exit_row)

    solved = []
    for row in maze:
        line = ''.join(row)
        solved.append(line)
    return '\n'.join(solved)
