import csv
import time

from diffprivacy import dict, neo4jdriver

record_time = False


# creates indexes for the labels
def create_index(label, label_id):
    if record_time:
        start = time.time()

    print("create_index start")
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dict.index_query_create.format(label, label_id))


    print("create_index end")

    if record_time:
        end = time.time()
        print(end - start)


def create_movies():
    data = []
    if record_time:
        start = time.time()

    print("create_movies start")
    with open(dict.movie_csv, 'r') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[0]), "title": row[1], "genres": row[2]})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(dict.movie_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dict.movie_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_movies end")

    if record_time:
        end = time.time()
        print(end - start)


def create_links():
    data = []
    if record_time:
        start = time.time()

    print("create_links start")
    with open(dict.link_csv, 'r') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[0]), "imdbId": row[1], "tmdbId": row[2]})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(dict.link_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dict.link_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_links end")

    if record_time:
        end = time.time()
        print(end - start)


def create_ratings():
    data = []
    if record_time:
        start = time.time()

    print("create_ratings start")
    with open(dict.rating_csv, 'r') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[1]), "user_id": int(row[0]), "rating": float(row[2]), "timestamp": row[3]})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(dict.rating_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dict.rating_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_ratings end")

    if record_time:
        end = time.time()
        print(end - start)


def create_tags():
    data = []
    if record_time:
        start = time.time()

    print("create_tags start")
    with open(dict.tag_csv, 'r') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[1]), "user_id": int(row[0]), "tag": row[2], "timestamp": float(row[3])})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(dict.tag_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dict.tag_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_tags end")

    if record_time:
        end = time.time()
        print(end - start)


# get movie by id
def get_movie_by_id(movie_id):
    if record_time:
        start = time.time()

    print("return_movie start", movie_id)
    with neo4jdriver.session.begin_transaction() as tx:
        print("start query")
        records = tx.run(dict.movie_query_get_by_id, movie_id=movie_id)
        data= records.data()
        print("start query",data)
        if not len(data):
            print ("No record!")
        else:

            for record in data:
                title = record["m"]["title"]
                print("return_movie title")
                print(title)
    print("return_movie end")

    if record_time:
        end = time.time()
        print(end - start)


# get average of ratings of specific movie
def get_avg_rating_of_movie(movie_id):
    if record_time:
        start = time.time()

    print("get_avg_rating_of_movie start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dict.movie_query_get_avg_rating, movie_id=movie_id)
        data= records.data()
        print (data)
        if not len(data):
            print ("No record!")
        else:
            for record in data:
                title = record["title"]
                avg = record["rating_avg"]
                print("%s has %s average rating" % (title, avg))
    # print("get_avg_rating_of_movie end")

    if record_time:
        end = time.time()
        print(end - start)


# get average of ratings of users
def get_avg_rating_of_user(user_id):
    if record_time:
        start = time.time()

    # print("get_avg_rating_of_user start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dict.user_query_get_avg_rating, user_id=user_id)
        rating_mean = 0
        data= records.data()
        if not len(data):
            print ("No record!")
        else:
            for record in data:
                # user_id = record["user_id"]
                rating_mean = record["rating_avg"]
                print("%s has %s average rating" % (user_id, rating_mean))
    # print("get_avg_rating_of_user end")

    if record_time:
        end = time.time()
        print(end - start)

    return rating_mean


# get average of ratings of all users
def get_avg_rating_of_all_user():
    if record_time:
        start = time.time()

    users_rating_avg = {}
    # print("get_avg_rating_of_user start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dict.user_query_get_all_avg_rating)
        if not len(records.data()):
            print ("No record!")
        else:
            for record in records:
                user_id = record["user_id"]
                rating_mean = record["rating_avg"]
                users_rating_avg[user_id] = rating_mean
    # print("get_avg_rating_of_user end")

    if record_time:
        end = time.time()
        print(end - start)

    return users_rating_avg


#
def create_dynamic_similarity(data):
    if record_time:
        start = time.time()

    print("create_dynamic_similarity start")
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dict.movie_query_create_dynamic_similarity, data=data)
        tx.commit()
    print("create_dynamic_similarity end")

    if record_time:
        end = time.time()
        print(end - start)


#
def create_static_similarity():
    pass


#
def get_all_movies():
    pass


#
def get_by_ratings_movie_ids(movie1_id, movie2_id):
    if record_time:
        start = time.time()

    print("get_by_ratings_movie_ids start", movie2_id, movie1_id)
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dict.movie_movie_query_adjusted_cosine, movie1_id=movie1_id, movie2_id=movie2_id)
    print("get_by_ratings_movie_ids end")
    data =records.data()
    print (data)
    if record_time:
        end = time.time()
        print(end - start)

    return data


# get count of movie
def get_movie_ids():
    if record_time:
        start = time.time()

    data = []
    # print("get_movie_count start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dict.movie_query_get_all_movie_ids)
        for record in records:
            data.append(record["movie_id"])
    # print("get_movie_count end")

    if record_time:
        end = time.time()
        print(end - start)

    return data

def get_movies_for_users_who_watched_by_id(movie_id):
    if record_time:
        start = time.time()

    print("get_reviews_for_rating_including_text start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dict.users_who_watched_also_watched_by_id,movie_id=movie_id)
        data =records.data()
        print("get_prediction", data)



    if record_time:
        end = time.time()
        print(end - start)

    return data
def get_movies_for_users_who_watched(title):
    if record_time:
        start = time.time()

    print("get_reviews_for_rating_including_text start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dict.users_who_watched_also_watched,title=title)
        data =records.data()
        print("get_prediction", data)



    if record_time:
        end = time.time()
        print(end - start)

    return data
def get_reviews_for_rating_including_text(title_includes):
    if record_time:
        start = time.time()

    print("get_reviews_for_rating_including_text start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dict.movie_ratings_by_title_includes,title_includes=title_includes)
        data =records.data()
        print("get_prediction", data)



    if record_time:
        end = time.time()
        print(end - start)

    return data
# returns list of (otherMovieId, similarity) of movie
def get_prediction_by_user_and_movie_id(user_id, movie_id, k_neighbours=5):
    if record_time:
        start = time.time()

    print("get_prediction_by_user_and_movie_id start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dict.user_movie_query_get_prediction,movie_id=movie_id, user_id=user_id, k_neighbours=k_neighbours)
        data =records.data()
        print("get_prediction", data)
        for record in data:
            prediction = record["prediction"]


    if record_time:
        end = time.time()
        print(end - start)

    return prediction


# get movie rating count by movie id
def get_movie_rating_count(movie_id):
    count = -1
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dict.movie_rating_count_query_by_id, movie_id=movie_id)
        data = records.data()
        if not len(data):
            print ("No record!")
        else:
            # privacy
            count = data[0]['count']
    return count
