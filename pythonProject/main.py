
from diffprivacy.MF_recommender import Matrix_Factorization
from eval import evaluator

import pandas as pd


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Recsys')
    train = pd.read_csv('dataset/ml-100k/test_rating.csv', index_col=0)
    test = pd.read_csv('dataset/ml-100k/user-rating_test.csv', index_col=0)
    MF_estimate = Matrix_Factorization.Matrix_Factorization(K=3, epoch=10,beta=0.06)
    MF_estimate.fit(train)
    R_hat = MF_estimate.start()
    non_index = test.values.nonzero()
    pred_MF = R_hat[non_index[0], non_index[1]]
    actual = test.values[non_index[0], non_index[1]]
    print('MSE of MF is %s' % evaluator.comp_mse(pred_MF, actual))
    print('RMSE of MF is %s' % evaluator.comp_rmse(pred_MF, actual))