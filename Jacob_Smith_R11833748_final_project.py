#!/usr/bin/env python3
"""
=============================================================================
Title : example.py
Description : This is an example script.
Author : errees (R#123456)
Date : 01/01/2001
Version : 1.0
Usage : python3 example.py
Notes : This example script has no requirements.
Python Version: 3.x.x
=============================================================================
"""
import copy
import multiprocessing
import sys
from multiprocessing import Pool, Process, Array
import ctypes

# defines global variables:
neighborValues = {'O':2, 'o':1, '.':0, 'x':-1, 'X':-2}
primeNumbers = {2, 3, 5, 7, 11, 13}
powerOf2Numbers = {1,2,4,8,16}

# this returns the arguments provided in the command line as tuple
def readArgs():
    args = sys.argv[1:]
    argList = args[::2]
    paramList = args[1::2]
    args = zip(argList, paramList)
    inputFile = None
    outputFile = None
    threadCount = 1
    for f, val in args:
        if f=='-i':
            inputFile = val
        elif f=='-o':
            outputFile = val
        elif f=='-p':
            threadCount = val
    return inputFile, outputFile, threadCount


# this read the matrix and returns it 
def makeMatrix(file):
    matrix=[]
    try:
        f = open(str(file), "r")
    except FileNotFoundError: 
        print("Error with file path")
    for line in f:
        matrix.append(list(line.strip()))
    f.close()
    return matrix


def printOutMatrix(matrix, fileout):
    f = open(fileout, 'w')
    for line in matrix:
        f.write(''.join(line))
        f.write('\n')
    f.close()

# this handles the logic of how to actually start running what types of code to run
def main():
    print('Project :: R11833748')
    inputFile, outputFile, threadCount = readArgs()
    matrix = makeMatrix(inputFile)
    finalSerial = cereal(matrix)
    if int(threadCount) == 1:
        printOutMatrix(finalSerial, outputFile)
    else:
        printOutMatrix(concurrency(matrix, int(threadCount)), outputFile)


# this calculates current cell values based on neigboring cells
def calcVal(matrix, row, col):
    ret = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(matrix) and 0 <= c < len(matrix[0]): 
            ret+=neighborValues[matrix[r][c]]
    return ret


# this method runs the serial execution of the code
def cereal(matrix):
    updatedMatrix = [[None for x in range(len(matrix[0]))] for y in range(len(matrix))]
    temp = matrix
    for i in range(100):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                val = calcVal(temp, i, j) 
                updatedMatrix[i][j] = updateCell(matrix[i][j],val)
        temp = copy.deepcopy(updatedMatrix)
        
    return updatedMatrix


def f(pos, diff, matrix):
    temp = []
    for i in range(pos, pos + diff):
        r = i // len(matrix[0])
        c = i % len(matrix[0])
        val = calcVal(matrix, r, c)
        temp.append(updateCell(matrix[r][c],val))
    return temp



def concurrency(matrix, threadCount):
    row, col = len(matrix), len(matrix[0])
    totalElements = row * col
    if threadCount < totalElements:
        diff = totalElements // threadCount
        differences = [diff] * threadCount
        extra = totalElements % threadCount
        for i in range(extra):
            differences[i] += 1
    else:
        differences = [1] * totalElements

    pos = 0
    for i,diff in enumerate(differences):
        differences[i] = [pos, diff, matrix]
        pos+=diff

    pool = Pool(processes=len(differences))
    updatedMatrix = matrix
    chunks = differences
    for x in range(100):
        linearArr = pool.starmap(func=f, iterable=chunks)
        currIndex=0
        for currList in linearArr:
            for currElement in currList:
                i,j = currIndex//col, currIndex%col
                updatedMatrix[i][j] = currElement
                currIndex+=1

        for i in range(len(chunks)):
            chunks[i][2] = updatedMatrix

    pool.close()
    return updatedMatrix


def updateCell(type, val):
    if type == 'O':
        if val>0 and val in powerOf2Numbers:
            return '.'
        if val<10:
            return 'o'
        return 'O'
    if type == 'o':
        if val<=0:
            return '.'
        if val >=8:
            return 'O'
        return 'o'
    if type == '.':
        if val>0 and val in primeNumbers:
            return 'o'
        if abs(val) in primeNumbers:
            return 'x'
        return '.'
    if type == 'x':
        if val>=1:
            return '.'
        if val<=-8:
            return 'X'
        return 'x'
    if type == 'X':
        if abs(val) in powerOf2Numbers:
            return '.'
        if val >-10:
            return 'x'
        return 'X'



if __name__ == '__main__':
    main()

    
