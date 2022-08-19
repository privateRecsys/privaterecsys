### Hi there 👋

By using any service online, or just by interacting in the Internet you produce data, which you may not realise at the beginning but putting them together can reveal sensitive and private information regarding you and your interests, your thoughts, your intentions. (e.g. movie ratings, medical records, e-mail patterns). 
These data can be useful for improving your online experience, for making sure that you find relevant articles to read, and helpful sources of information but also finding the products you want to buy and visiting the restaurants that match your taste.

There is a need for a way to have an intellligent and efficient internet, while at the same time protect your identity and have your privacy in mind.
Anonymisation techniques, have been used as a method of preserving real identities.. however, research has shown that deanonymization can easily be achived by combining multple sources of information.


## Privacy Preserving Approach 1:  Differential Privacy 
Differential privacy aims to provide means to maximize the accuracy of these statistical queries while minimizing the chances of identifying its records. It introduces noise to real data so that, adding or removing one user to database does not make noticeable difference in the data, thus preventing to identify his/her private information. It is a probabilistic concept, therefore, any differentially private mechanism is necessarily randomized with Laplace mechanism, exponential mechanism etc.

Let ε be a positive real number and A be a randomized algorithm that takes a dataset as input (representing the actions of the trusted party holding the data). The algorithm A is ε-differentially private if for all datasets 𝐷_1 and 𝐷_2 that differ on a single element (i.e., the data of one person), and all subsets S of image of A.

![ε-differential privacy formula](Documentation/formula.png)


where the probability is taken over the randomness used by the algorithm.

Differential privacy is used in this implementation of the privacy recsys.
### Differencial Privacy Example 1  -  Movie recommendation
For the first test of this approach, a publicly available movie ratings dataset has been considered, and by using the ratings of the users, most similar movies to user’s ratings is determined and a suitable recommendation is done from the ones among them.
The dataset is processed using a graph database (Neo4j), which allows to represent users and movies as nodes and as edges betweeen them the rating a user has given to a movie as well as the similarity between two nodes (in this case two movies).
Below, a snapshot from the represenation of a subset of the database is provided. Orange nodes are anonymized users, Purple nodes are movies and the edges are rating(numeric score) and tag(comment) relations between users and movies.


![Graph Representation of nodes and edges](Documentation/snapshot.png)


### DiffPrivacy - Privacy Recsys Test Results
note: please start node4j graph server before running the scripts. 

To measure the error of the recommendation algorithm, and determine the privacy/utility ratio  of the recommendation we undertake a small evaluation based on thequery "What is the number of ratings given to a movie? (movie name as parameter) considering all the data in our dataset" is shown. This is the fundamental question for testing the effectiveness of differential privacy - according to which you should never be able to determine how many users have contributed for this rating and therefore removing all ratings -1 will not return the rating of the one user that remained. The Algorithm is run three times and all results are included to the table. The difference in the results is attributed to the randomness of the algorithm, and the application of differntial privacy as noise.

 

| Movie ID | Actual Rating Count | 	Noisy Rating Count (exp-1)  | 	Noisy Rating Count (exp-2)  | 	Noisy Rating Count (exp-3)  |
|---|---|---|---|---|
| 5 | 51| 61.53068160858365 |  4.14780634816978 |45.74972097598749 |
| 8 | 8 | 23.754713618664823| 4.5610873458316625 | -30.184266258323568 |
| 9 | 16 | 3.8271299734101802| 16.430418771569318 | 5.221803446422436|
| 11| 72 | 80.61785730156829| 68.2613306805804| 90.99006185916669 |
| 210 | 4 | 12.93616669892703| -1.441247061146698 | -26.601274325745656|

- To run this experiment - run the "main.py" within the diffprivacy/differential_privacy folder.
- To test on a small sample use the scripts within the diffprivacy/benchmark folder.
- To produce recommendations on popularity (average rating) and also privacy-presevring collaborative filtering run "main.py" within the diffprivacy/lens folder.

### Web Application

## Node API
First, configure your api/.env file to point to your database.

Then, from the root directory of this project:
```
cd api
nvm use
npm install
node app.js starts the API

```
## Frontend
From the root directory of this project, set up and start the frontend with:
```
cd web
nvm use
update web/.env file
```
If you are using the Node API set REACT_APP_API_BASE_URL to http://localhost:3000/api/v0

If you are using the Flask api then set it to http://localhost:5000/api/v0
```
yarn 
yearn start starts the app on http://localhost:3000/
```
