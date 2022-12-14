########################################################
# utils.py
# This is a script containing a bag of utilities.
# Author: Jamie Zhu <jimzhu@GitHub>
# Created: 2014/2/6
# Last updated: 2015/8/17
########################################################


import os, sys, time
import logging
import numpy as np


# ======================================================#
# Function to set configuartions and set up logging
# ======================================================#
def setConfig(para):
    config = {'exeFile': os.path.basename(sys.argv[0]),
              'workPath': os.path.abspath('.'),
              'dataPath': os.path.abspath(para['dataPath'])
              }

    # add result folder
    if not os.path.exists(para['outPath']):
        os.makedirs(para['outPath'])

    # set up logging to record runtime info
    level = logging.INFO
    if para['debugMode']:
        level = logging.DEBUG
    logging.basicConfig(level=level,
                        disable_existing_loggers=False,
                        format='%(asctime)s (pid-%(process)d): %(message)s')

    logging.info('==========================================')
    logging.info('configs as follows:')
    config.update(para)
    for name in config:
        if type(config[name]) is np.ndarray:
            logging.info('%s = [%s]' % (name, ', '.join(format(s, '.2f') for s in config[name])))
        else:
            logging.info('%s = %s' % (name, config[name]))

    # set print format
    np.set_printoptions(formatter={'float': '{: 0.4f}'.format})


# ======================================================#
# Formatting the elapsed time into day-hour-min-sec format
# ======================================================#
def formatElapsedTime(elapsedtime):
    minutes, seconds = divmod(elapsedtime, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365.242199)

    minutes = long(minutes)
    hours = long(hours)
    days = long(days)
    years = long(years)

    duration = ''
    if years > 0:
        duration += ('%d year' % years + 's' * (years > 1) + ', ')
    if days > 0:
        duration += ('%d day' % days + 's' * (days > 1) + ', ')
    if hours > 0:
        duration += ('%d hour' % hours + 's' * (hours > 1) + ', ')
    if minutes > 0:
        duration += ('%d minute' % minutes + 's' * (minutes > 1) + ', ')
    if seconds > 0:
        duration += ('%.2f second' % seconds + 's' * (seconds > 1) + '.')
    return duration