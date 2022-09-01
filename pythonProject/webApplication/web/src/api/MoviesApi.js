import settings from '../config/settings';
import axios from './axios';
import _ from 'lodash';

const {apiBaseURL} = settings;

export default class MoviesApi {
  static getGenres() {
    return axios.get(`${apiBaseURL}/genres`);
  }

  // convert this to top 3 most rated movies
  // axios.get(`${apiBaseURL}/movies/15602`)
  static getMovies() {
    return Promise.all([
      axios.get('http://localhost:5000/api/v0/movies/862'),
      axios.get('http://localhost:5000/api/v0/movies/8844'),

    ]);
  }
 
  static getMoviesByGenres(genreNames) {
    return MoviesApi.getGenres()
      .then(genres => {
        var movieGenres = _.filter(genres, g => {
          return genreNames.indexOf(g.name) > -1;
        });

        return Promise.all(
          movieGenres.map(genre => {
              return axios.get(`${apiBaseURL}/movies/genre/${genre.id}/`);
            }
          ))
          .then(genreResults => {
            var result = {};
            genreResults.forEach((movies, i) => {
              result[movieGenres[i].name] = movies;
            });

            return result;
          });
      });
  }

  // convert this to top 3 most rated movies
  static getFeaturedMovies() {
   return Promise.all([
      axios.get(`${apiBaseURL}/movies/862`),
      axios.get(`${apiBaseURL}/movies/8844`),
      axios.get(`${apiBaseURL}/movies/15602`)
    ]);
  }

  static getMovie(id) {
      return axios.get(`${apiBaseURL}/movies/${id}`);
  }

  static rateMovie(id, rating) {
    return axios.post(`${apiBaseURL}/movies/${id}/rate`, {rating});
  }

  static deleteRating(id) {
    return axios.delete(`${apiBaseURL}/movies/${id}/rate`);
  }
}


