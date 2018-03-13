import React from 'react';

export class ResourceFilterOption extends React.Component {
  constructor() {
    super();

    this.filterClick = this.filterClick.bind(this);
  }

  filterClick() {
    this.props.handleClick(this.props.filter)
  }

  render() {
    return (
      <span
        className={this.props.className}
        onClick={this.filterClick}>
        {this.props.filter}
      </span>
    );
  }
}
