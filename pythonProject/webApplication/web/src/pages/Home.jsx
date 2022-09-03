import React from 'react';
import { Link } from 'react-router-dom';
import Loading from '../components/Loading.jsx';
import Carousel from '../components/Carousel.jsx';
import _ from 'lodash';

import * as MovieActions from '../redux/actions/MovieActions';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

class Home extends React.Component {
  constructor() {
    super();

   this.renderFeatured = this.renderFeatured.bind(this);
   // this.renderByGenre = this.renderByGenre.bind(this);
  }

  componentWillMount() {
  this.props.getFeaturedMovies();
 //

  // this.props.getMoviesByGenres(['Adventure', 'Drama']);
  }

  render() {
    var {movies} = this.props;

    return (
      <div className="container">

            {movies.isFetching ? <Loading/> : null}
            {this.renderFeatured()}
          </div>

    );
  }

  renderFeatured() {
    var {movies} = this.props;
    return (
      <div className="display-1">
        <h1 className="display-1">Latest Movies</h1>
    <Carousel>
          { _.compact(movies.featured).map(m => {
           return (
                <div key={m.id}>
                  <Link to={`/movie/${m.id}`}>
                    <img src={m.posterImage} alt="" />
                  </Link>
                  <div className="nt-carousel-movie-title">
                    <Link to={`/movie/${m.id}`}>{m.title}</Link>
                  </div>
                </div>
              );
          })}
        </Carousel>
      </div>
    );
  }

  renderByGenre(name) {
    var {movies} = this.props;
    var moviesByGenre = movies.byGenre[name];

    if (_.isEmpty(moviesByGenre)) {
      return null;
    }

    return (
      <div className="nt-home-by-genre">
        <div className="nt-box">
          <div className="nt-box-title">
            {name}
          </div>
          <Carousel>
            { moviesByGenre.map(m => {
              return (
                <div key={m.data.id}>
                  <Link to={`/movie/${m.data.id}`}>
                    <img src={m.posterImage} alt="" />
                  </Link>
                  <div className="nt-carousel-movie-title">
                    <Link to={`/movie/${m.data.id}`}>{m.data.title}</Link>
                  </div>
                </div>
              );
            })}
          </Carousel>
        </div>
      </div>);
  }
}
Home.displayName = 'Home';

function mapStateToProps(state) {
  return {
    genres: state.genres.items,
    movies: state.movies
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(MovieActions, dispatch);
}

// Wrap the component to inject dispatch and state into it
export default connect(mapStateToProps, mapDispatchToProps)(Home);