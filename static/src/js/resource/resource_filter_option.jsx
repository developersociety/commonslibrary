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
        <svg className="icon">
            <use xlinkHref={"#" + this.props.filter}></use>
        </svg>
      </span>
    );
  }
}
