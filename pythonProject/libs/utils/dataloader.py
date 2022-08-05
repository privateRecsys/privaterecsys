########################################################
# dataloader.py
# Author: PrivX<privaterecsys@GitHub>
# Created: 2022/08/05
# Last updated: 2022/08/05
########################################################


import numpy as np
import logging
import os


#======================================================#
# Function to load the dataset
#======================================================#
def load(para):
    datafile = para['dataPath'] + para['dataName'] + '/' + para['dataType'] + 'Matrix.txt'
    logging.info('Loading data: %s'%os.path.abspath(datafile))
    dataMatrix = np.loadtxt(datafile)
    dataMatrix = preprocess(dataMatrix, para)
    logging.info('Data size: %d users * %d services'\
        %(dataMatrix.shape[0], dataMatrix.shape[1]))
    logging.info('Loading data done.')
    logging.info('----------------------------------------------')
    return dataMatrix


#======================================================#
# Function to preprocess the dataset which
# deletes the invalid values
#======================================================#
def preprocess(matrix, para):
    if para['dataType'] == 'rt':
        matrix = np.where(matrix == 0, -1, matrix)
        matrix = np.where(matrix >= 20, -1, matrix)
    elif para['dataType'] == 'tp':
        matrix = np.where(matrix == 0, -1, matrix)
    return matrix
