import React from 'react';
import _ from 'lodash';
import Loading from '../components/Loading.jsx';
import Carousel from '../components/Carousel.jsx';
import UserRating from '../components/UserRating.jsx';
import {Link} from 'react-router-dom';
import * as MovieActions from '../redux/actions/MovieActions';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';


class Movie extends React.Component {
  componentDidMount() {
    var {id} = this.props.match.params;
    this.props.getMovie(id);
    //this.props.getSimilarMoviesById(id);
  }

  componentDidUpdate(prevProps) {
    if (prevProps.match.params.id !== this.props.match.params.id) {
      this.props.clearMovie();

      var {id} = this.props.match.params;
      this.props.getMovie(id);
    }
  }

  componentWillUnmount() {
    this.props.clearMovie();
  }

  render() {
    var {isFetching, movie, rateMovie, deleteMovieRating, profile} = this.props;

   console.log("movies2",movie)
    return (

      <div className="nt-movie">

        {isFetching ? <Loading/> : null}
        {movie ?
          <div>
            <div className="row">
              <div className="large-12 columns">
                <h2 className="nt-movie-title">{movie.data.title}</h2>
              </div>
            </div>
            <div className="row">
              <div className="small-12 medium-4 columns nt-movie-aside">
                <img className="nt-movie-poster"
                     src={movie.data.posterImage}
                     alt="" />

              </div>
              <div className="small-12 medium-8 columns nt-movie-main">
                <div>
                  {profile ?
                    <div className="nt-box">
                      <p className="nt-box-row nt-movie-rating">
                        <strong>Your rating: </strong>
                        <UserRating movieId={movie.data.id}
                                    savedRating={movie.data. myRating}
                                    onSubmitRating={rateMovie}
                                    onDeleteRating={deleteMovieRating}/>
                      </p>
                    </div>
                    :
                    null
                  }


                </div>
              </div>
              <div className="small-12 columns">
                <div className="nt-box">
                  <div className="nt-box-title">
                    Related Movies
                  </div>

                </div>
              </div>
            </div>
          </div>
          :
          null
        }
      </div>
    );
  }

  getKeywordsText(movie) {
    _.filter(movie.data.keywords, k => {
      return !!k.name;
    })
      .join(', ');
  }

  renderCast(actors) {
    if (_.isEmpty(actors)) {
      return null;
    }

    return (
      <Carousel>
        {
          actors.map(a => {
            return (
              <div key={a.id}>
                <Link to={`/person/${a.id}`}>
                  <img src={a.posterImage} alt="" />
                </Link>
                <div className="nt-carousel-actor-name"><Link to={`/person/${a.id}`}>{a.name}</Link></div>
                <div className="nt-carousel-actor-role">{a.role}</div>
              </div>
            );
          })
        }
      </Carousel>);
  }
renderRelatedMovies() {
    var {movies} = this.props;
    return (
      <div className="nt-home-featured">
        <h3 className="nt-home-header">Private RecSys Movies</h3>

          { _.compact(movies.featured).map(m => {
           return (
                <div key={m.id}>
                  <Link to={`/movie/${m.data.id}`}>
                    <img src={m.posterImage} alt="" />
                  </Link>
                  <div className="nt-carousel-movie-title">
                    <Link to={`/movie/${m.data.id}`}>{m.data.title}</Link>
                  </div>
                </div>
              );
          })}

      </div>
    );
  }

  renderPeople(people) {
    return people.map((p, i) => {
      return (
        <span key={p.id}>
        <Link to={`/person/${p.id}`}>{p.name}</Link>
          {i < people.length - 1 ? <span>, </span> : null}
      </span>);
    });
  }

  renderGenre(genres) {
    return genres.map((g, i) => {
      return (<span key={g.id}>
        {g.name}
        {i < genres.length - 1 ? <span>, </span> : null}
      </span>);
    });
  }
}
Movie.displayName = 'Movie';

function mapStateToProps(state) {
  return {
    movie: state.movies.detail,
    isFetching: state.movies.isFetching,
    profile: _.get(state, 'profile.profile')
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(MovieActions, dispatch);
}

// Wrap the component to inject dispatch and state into it
export default connect(mapStateToProps, mapDispatchToProps)(Movie);
