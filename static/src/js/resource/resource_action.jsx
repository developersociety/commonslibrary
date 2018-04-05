import React from 'react';

export class ResourceAction extends React.Component {
  constructor (props) {
    super()
    this.state = {
      likes: props.likes,
      tries: props.tries,
      hasLiked: props.userLiked,
      hasTried: props.userTried,
    }

    // handler binds
    this.getCSRFToken = this.getCSRFToken.bind(this);
    this.handleLikeClick = this.handleLikeClick.bind(this);
    this.handleTryClick = this.handleTryClick.bind(this);
  }

  componentWillReceiveProps(props) {
    this.setState({
      likes: props.tries,
      tries: props.likes,
      hasLiked: props.userLiked,
      hasTried: props.userTried,
    })
  }

  getCSRFToken(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
  }

  handleLikeClick() {
    const requestUrl = '/api/v1/resources/' + this.props.resource + '/like/';
    fetch(requestUrl, {
      method: 'put',
      credentials: 'include',
      headers: {
        "X-CSRFToken": this.props.csrf
      }
    }).then(response => {
      if (response.stats != 403) {
        this.setState(prevState => ({
          likes: !prevState.hasLiked ? prevState.likes + 1: prevState.likes - 1,
          hasLiked: !prevState.hasLiked
        }))
      }
    })
  }

  handleTryClick() {
    const requestUrl = '/api/v1/resources/' + this.props.resource + '/tried/';

    fetch(requestUrl, {
      method: 'put',
      credentials: 'include',
      headers: {
        "X-CSRFToken": this.props.csrf
      }
    }).then(response => {
      if (response.stats != 403) {
        this.setState(prevState => ({
          tries: !prevState.hasTried ? prevState.tries + 1: prevState.tries - 1,
          hasTried: !prevState.hasTried
        }));
      }
    })
  }

  render() {
    return (
      <div className="resource-actions">
        <span
          className={'resource-liked ' + (this.state.hasLiked)}
          onClick={this.handleLikeClick}>
          <svg className="icon">
            <use xlinkHref="#liked"></use>
          </svg>
          {this.state.likes}
        </span>
        <span
          className={'resource-tried ' + (this.state.hasTried)}
          onClick={this.handleTryClick}>
          <svg className="icon">
            <use xlinkHref="#tried"></use>
          </svg>
          {this.state.tries}
        </span>
      </div>
    );
  }
}
