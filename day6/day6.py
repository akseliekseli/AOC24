import csv
import argparse
import re
import numpy as np
from collections import defaultdict
import copy
import time

class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()

    def data_to_matrix(self):
        matrix = []
        y_bound = len(self.lines)
        for ii, line in enumerate(self.lines):
            for jj in range(len(line)):
                x_bound = len(line)
                if line[jj]=='^':
                    startpoint = [ii, jj]
            matrix.append(list(line))
        
        ii, jj = startpoint[0], startpoint[1]
        print(str(matrix[ii])[jj])
        return matrix, ii, jj, y_bound, x_bound

    def first(self):
        self.matrix, ii, jj, self.rows, self.cols = self.data_to_matrix()
        matrix = copy.deepcopy(self.matrix)
        n_pos, matrix = self.traverse_matrix(matrix, ii, jj)
        return n_pos

    def traverse_matrix(self, matrix, ii, jj):
        '''
        This "himmeli" reminds me of Basics of Programming in Python course at LUT University
        '''
        dir = 0
        n_pos = 1
        self.loop = False
        visited_points_dir = set()
        while (ii>=0) and (ii<self.rows) and (jj >=0) and (jj < self.cols):
            if ((ii, jj, dir)) in visited_points_dir:
                self.loop = True
                return n_pos, matrix
            else:
                visited_points_dir.add((ii, jj, dir))
            try:
                if dir==0:
                    if matrix[ii-1][jj]=='#':
                        dir = 1
                    else:
                        ii -= 1
                        if matrix[ii][jj]=='X':
                            pass
                        else:
                            matrix[ii][jj]='X'
                            n_pos += 1
                elif dir==1:
                    if matrix[ii][jj+1]=='#':
                        dir = 2
                    else:
                        jj += 1
                        if matrix[ii][jj]=='X':
                            pass
                        else:
                            matrix[ii][jj]='X'
                            n_pos += 1
                elif dir==2:
                    if matrix[ii+1][jj]=='#':
                        dir = 3
                    else:
                        ii += 1
                        if matrix[ii][jj]=='X':
                            pass
                        else:
                            matrix[ii][jj]='X'
                            n_pos += 1
                elif dir==3:
                    if matrix[ii][jj-1]=='#':
                        dir = 0
                    else:
                        jj -= 1
                        if matrix[ii][jj]=='X':
                            pass
                        else:
                            matrix[ii][jj]='X'
                            n_pos += 1
            except:
                break
        return n_pos, matrix
            

    def second(self):
        #self.graph = defaultdict(list) 
        # Directions as tuples
        #self.dir = [(1, 0), (0,1), (-1, 0), (0, -1)]
        self.matrix, starti, startj, self.rows, self.cols = self.data_to_matrix()
        _, self.matrix = self.traverse_matrix(self.matrix, starti, startj)
        xs = []
        for ii in range(0, self.rows):
            for jj in range(0, self.cols):
                if self.matrix[ii][jj] == 'X':
                    xs.append([ii, jj])
        loop_obstacles = set()
        self.loop = False
        for idx, x in enumerate(xs):
            print(f'Iteration: {idx}/{len(xs)}')
            new_matrix = copy.deepcopy(self.matrix)
            if (x[0]==starti) and (x[1]==startj):
                continue
            else:
                new_matrix[x[0]][x[1]] = '#'
                _, new_matrix = self.traverse_matrix(new_matrix, starti, startj)
            if self.loop:
                loop_obstacles.add(idx)
        return len(loop_obstacles)
        
if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('test', help="True/False")
    parser.add_argument('case', help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.case)
    test = True if args.test in ['True','true'] else False
    start = time.time()
    solution = Solution(test=test)
    results = solution.first() if case == 1 else solution.second()
    end = time.time()
    print(f'Results part {case}: {results}')
    print(f'Runtime: {end-start}')
