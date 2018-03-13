import React from 'react';

export class ResourceAction extends React.Component {
  constructor (props) {
    super()
    this.state = {
      likes: props.tries,
      tries: props.likes,
      hasLiked: false,
      hasTried: false,
    }

    // handler binds
    this.handleLikeClick = this.handleLikeClick.bind(this);
    this.handleTryClick = this.handleTryClick.bind(this);
  }

  componentWillReceiveProps(props) {
    this.setState({
      likes: props.tries,
      tries: props.likes,
    })
  }

  handleLikeClick() {
    this.setState(prevState => ({
      likes: !prevState.hasLiked ? prevState.likes + 1: prevState.likes - 1,
      hasLiked: !prevState.hasLiked,
    }));
  }

  handleTryClick() {
    this.setState(prevState => ({
      tries: !prevState.hasTried ? prevState.tries + 1: prevState.tries - 1,
      hasTried: !prevState.hasTried,
    }));
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
