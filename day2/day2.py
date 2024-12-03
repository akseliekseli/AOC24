import csv
import argparse
import numpy as np


class Solution:
    input_filename = 'input.txt'
    input_filename_test = 'example.txt'

    def __init__(self, test=False):
        self.file = open(self.input_filename_test,'r').read() if test else open(self.input_filename,'r').read()
        self.lines = self.file.splitlines()


    def first(self):
        n_safe = 0
        for item in self.lines:
            values = list(map(int, item.split()))

            diffs = np.diff(values)
            print(values)
            if (all(i < j for i, j in zip(values, values[1:])) or all(i > j for i, j in zip(values, values[1:]))) and np.abs(diffs).max()<4:
                print('Safe')
                n_safe = n_safe+1
        return n_safe


    def second(self):
        n_safe = 0
        for item in self.lines:
            values = list(map(int, item.split()))

            diffs = np.diff(values)
            print(values)
            increasing, decreasing = self.check_increasing(values)
            if (increasing or decreasing) and np.abs(diffs).max()<4:
                print('Safe')
                n_safe = n_safe+1
            else:
                positives = sum(1 for i in diffs if i >0)
                negatives = sum(1 for i in diffs if i <0)
               #print(positives, negatives)
                #if sum(diffs) == 0:
                #    print('HERE')
                #    continue
                if ((diffs==0).sum() == 1):
                    values = list(self.unique(values))
                elif positives == negatives:
                    continue
                elif (positives > negatives) and (negatives ==1):
                    idx = (np.nonzero(diffs<0)[0][0])
                    if idx == len(diffs)-1:
                        values.pop(idx+1)
                    elif idx*2 > len(diffs):
                        values.pop(idx+1)
                    else:
                        values.pop(idx)
                elif (positives < negatives) and (positives == 1):
                    idx = (np.nonzero(diffs>0)[0][0])
                    if idx == len(diffs)-1:
                        values.pop(idx+1)
                    elif idx*2 > len(diffs):
                        values.pop(idx+1)
                    else:
                        values.pop(idx)
                elif ((diffs>3).sum() == 1):
                    values.pop(np.nonzero(diffs>0)[0][0])
                print(f'values: {values}')
                increasing, decreasing = self.check_increasing(values)
                diffs = np.diff(values)
                if (increasing or decreasing) and np.abs(diffs).max()<4:
                    print('Safe')
                    n_safe = n_safe+1


            '''
            sorted_list = np.sort(values)
            sorted_desc = sorted_list[::-1]
            sorted_diff = np.diff(sorted_list)

            bad_levels = np.min([(values != sorted_list).sum(), (values != sorted_desc).any().sum()])
            bad_levels_idx = np.argmin(([np.abs(values-sorted_list).sum(), np.abs(values-sorted_desc).sum()]))
            same_levels = (sorted_diff==0).sum()

            if ((values == sorted_list).all() or (values == sorted_desc).all()) and (np.abs(sorted_diff)<4).all() and (sorted_diff != 0).all():
                n_safe = n_safe +1
            elif bad_levels+same_levels==1:
                print(f'Values original: {values}')
                if bad_levels == 1:
                    if bad_levels_idx == 0:
                        print(f'idx_1: {[i for i, x in enumerate((values!=sorted_list)) if x]}')
                        values.pop([i for i, x in enumerate((values!=sorted_list)) if x][0])
                        print(values)
                    elif bad_levels_idx == 1:
                        print(f'idx_2 {values}')
                        values.pop([i for i, x in enumerate((values!=sorted_desc)) if x][0])
                elif same_levels==1:
                    print(same_levels)
                    values = list(self.unique(values))
                print(f'Values removed: {values}')

                sorted_list = np.sort(values)
                sorted_desc = sorted_list[::-1]
                sorted_diff = np.diff(sorted_list)

                if ((values == sorted_list).all() or (values == sorted_desc).all()) and (np.abs(sorted_diff)<4).all() and (sorted_diff != 0).all():
                    print('Safe')
                    n_safe = n_safe +1
        '''
        return n_safe

    def check_increasing(self, values):
        increasing =(all(i < j for i, j in zip(values, values[1:])))
        decreasing =(all(i > j for i, j in zip(values, values[1:])))
        return increasing, decreasing

    def unique(self,sequence):
        seen = set()
        return [x for x in sequence if not (x in seen or seen.add(x))]


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('test', help="True/False")
    parser.add_argument('case', help="task 1: 1, task 2: 2")
    args = parser.parse_args()
    case = int(args.case)
    test = True if args.test in ['True','true'] else False
    solution = Solution(test=test)
    results = solution.first() if case == 1 else solution.second()

    print(f'Results part {case}: {results}')
