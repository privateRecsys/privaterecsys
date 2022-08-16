from diffprivacy import db
import csv
import time

base_dir = "../../dataset/"
subfolder = "ml-latest-small/"

_TEST_RATIO = 0.2
_k_neighbours = 5


def predict(user_id, movie_id):
    return db.get_prediction_by_user_and_movie_id(user_id, movie_id, _k_neighbours)


def avg_error():
    error_sum, count = 0, 0
    with open(base_dir + subfolder + "ratings_test_{}.csv".format(_TEST_RATIO)) as r_test:
        csvr = csv.DictReader(r_test, delimiter=',', quotechar='"')

        for row in csvr:
            print('row', row)
            prediction = predict(int(row["userId"]), int(row["movieId"]))
            print('row', prediction)
            if prediction != -1:
                count += 1
                error_sum += abs(prediction - float(row["rating"]))
    return error_sum / count if count > 0 else None


if __name__ == '__main__':
    start = time.time()
    error = avg_error()
    end = time.time()
    print ('Mean Average Error is', error)
    print ("Execution time: ", end - start)
