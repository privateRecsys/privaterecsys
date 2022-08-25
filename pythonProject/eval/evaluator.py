import numpy as np


def cos_measure(feature_vector, feature_matrix):
    x_c = (feature_vector * feature_matrix.T) + 0.0000001
    mod_x = np.sqrt(feature_vector * feature_vector.T)
    mod_c = np.sqrt((feature_matrix * feature_matrix.T).diagonal())
    cos_xc = x_c / (mod_x * mod_c)

    return cos_xc


def comp_mse(pred, actual):
    error = pred - actual
    count = error.nonzero()[0].shape
    MSE = (error).dot((error).T) / count
    return MSE

def comp_rmse(pred, actual):

    error = pred - actual
    count = error.nonzero()[0].shape
    RMSE = np.sqrt((error).dot((error).T) / count)
    return RMSE