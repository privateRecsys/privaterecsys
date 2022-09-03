import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

export default class Breadcrumbs extends React.Component {
  render() {
    var {auth, profile, movie, person} = this.props;

    return (
      <ul className="breadcrumbs">
        <li><Link to="/" className={movie ? '' : 'current'}>Home</Link></li>

         {
          profile ?
            <li><Link to="/profile" className={movie ? '' : 'current'}>Profile</Link></li>
            : null
        }
        {
          movie ?
            <li><Link to={`/movie/${movie.id}`} className="current">{movie.title}</Link></li>
            : null
        }
        {
          person ?
            <li><Link to={`/person/${person.id}`} className="current">{person.name}</Link></li>
            : null
        }
      </ul>
    );
  }
}

Breadcrumbs.displayName = 'Breadcrumbs';
Breadcrumbs.propTypes = {
  movie: PropTypes.object,
  person: PropTypes.object
};
