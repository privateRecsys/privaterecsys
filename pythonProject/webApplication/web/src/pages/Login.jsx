import React from 'react';
import PropTypes from 'prop-types';
import {withRouter} from 'react-router';
import {Link} from 'react-router-dom';
import InputValidator from '../components/validation/InputValidator.jsx';
import ValidatedComponent from '../components/validation/ValidatedComponent.jsx';
import * as Actions from '../redux/actions/AuthActions';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';

class Login extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      username: '',
      password: '',
      canSubmit: false
    };

    this.popup = null;

    this.changeUser = this.changeUser.bind(this);
    this.changePassword = this.changePassword.bind(this);
    this.login = this.login.bind(this);
    this.redirectIfAuthed = this.redirectIfAuthed.bind(this);
  }

  login(e) {
    e.preventDefault();

    if (this.props.isComponentValid()) {
      this.props.login(this.state.username, this.state.password);
    }
  }

  componentDidMount() {
    this.redirectIfAuthed(this.props);
  }

  componentWillReceiveProps(nextProps) {
    this.redirectIfAuthed(nextProps);
  }

  redirectIfAuthed(props) {
    var {token, match, history} = props;
    if (token) {
      if (match.params.redirectTo) {
        history.push(match.params.redirectTo);
      }
      else {
        history.push('/');
      }
    }
  }

  render() {
    var {username, password, canSubmit} = this.state;
    var {errors} = this.props;

    return (

    <div className="Auth-form-container">
        <form className="Auth-form">
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Log in</h3>
            <div className="text-center">
             Not registered yet?    <a href="/SignUp"> Sign up</a>
            </div>
            <div className="form-group mt-3">
             <InputValidator fieldName="User name"
                              errors={errors.username}
                              shouldValidateOnBlur={true}>
                <input type="text"
                       placeholder="User name*"
                       required
                       value={username}
                       onChange={this.changeUser}/>
              </InputValidator>
            </div>
            <div className="form-group mt-3">
             <InputValidator fieldName="Password"
                              errors={errors.password}
                              shouldValidateOnBlur={true}>
                <input type="password"
                       name="password"
                       placeholder="Password*"
                       required
                       value={password}
                       onChange={this.changePassword}/>
                       </InputValidator>
            </div>
            <div className="d-grid gap-2 mt-3">

              <button className="btn btn-primary"
                      type="submit"
                      name="submit-login"
                      onClick={this.login}
                      disabled={!canSubmit}>
                Log In
              </button>
            </div>
              <p className="text-center mt-2">
              Forgot <a href="#">password?</a>
            </p>
          </div>
        </form>
      </div>

    );
  }

  changeUser(event) {
    var canSubmit = this.state.password && event.target.value;
    this.setState({
      username: event.target.value,
      canSubmit: canSubmit
    });
  }

  changePassword(event) {
    var canSubmit = this.state.username && event.target.value;
    this.setState({
      password: event.target.value,
      canSubmit: canSubmit
    });
  }
}

Login.displayName = 'Login';

Login.propTypes = {
  query: PropTypes.object
};

function mapDispatchToProps(dispatch) {
  return bindActionCreators(Actions, dispatch);
}

function mapStateToProps(state) {
  return {...state.auth};
}

export default connect(mapStateToProps, mapDispatchToProps)(ValidatedComponent(withRouter(Login)));
