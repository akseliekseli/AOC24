import csv
import argparse
import re
import numpy as np
import copy
from collections import defaultdict
import time
import matplotlib.pyplot as plt

'''
Used modular arithmetic for the cell wrapping.
'''
class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()
        self.robots = defaultdict(list)
        for ii, line in enumerate(self.lines):
            numbers = re.findall(r'-?\d+', line)
            self.robots[ii] = [(int(numbers[0]), int(numbers[1])), (int(numbers[2]), int(numbers[3]))]
        pass

    def check_quadrant(self, point):
        (x, y) = point
        if x == self.cols//2 or y == self.rows//2: pass
        elif x < self.cols//2 and y < self.rows//2: self.quadrand_sums[0] += 1
        elif x < self.cols//2 and y > self.rows//2:  self.quadrand_sums[1] += 1
        elif x > self.cols//2 and y < self.rows//2:  self.quadrand_sums[2] += 1
        elif x > self.cols//2 and y > self.rows//2:  self.quadrand_sums[3] += 1

    def calculate_robot_positions(self, seconds):
        self.cols = 101
        self.rows = 103
        self.quadrand_sums = [0, 0, 0, 0]
        for key in self.robots.keys():
            x = (self.robots[key][0][0] + self.cols + seconds*self.robots[key][1][0]) % self.cols
            y = (self.robots[key][0][1] + self.rows + seconds*self.robots[key][1][1]) % self.rows
            self.robots[key][0] = (x, y)
            self.check_quadrant((x,y))

    def silver(self):
        seconds = 100
        self.calculate_robot_positions(seconds)
        result = 1
        for val in self.quadrand_sums:
            result = result*val
        return result
    
    def gold(self):
        seconds = 6400
        ii = 0
        self.robot_init = copy.deepcopy(self.robots)
        while True:
            self.robots = copy.deepcopy(self.robot_init)
            ii += 1
            self.calculate_robot_positions(seconds=seconds+ii)
            xs = [value[0] for key in self.robots for value in self.robots[key][:1]]
            ys = [value[1] for key in self.robots for value in self.robots[key][:1]]
            '''
            Used standard look from the image -method
            '''
            #plt.figure()
            #plt.scatter(xs,ys, s=20, c='k')
            #plt.show()
            #plt.savefig(f'{ii+seconds}.jpeg')
            #plt.close()
            # (Optional) Display intermediate steps for debugging
            print(f"Iteration {ii+seconds}")
            break # Comment this for plotting         
        pass


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('test', help="True/False")
    parser.add_argument('case', help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.case)
    test = True if args.test in ['True','true'] else False

    start = time.time()
    solution = Solution(test=test)
    results = solution.silver() if case == 1 else solution.gold()
    end = time.time()
    print(f'Results part {case}: {results}')
    print(f'Runtime: {end-start}')
