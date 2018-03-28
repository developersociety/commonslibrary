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
    let filterClass = 'resource-filter__option';

    if (this.props.active === this.props.filter) {
        filterClass = filterClass + ' active'
    }

    return (
      <span
        className={filterClass}
        onClick={this.filterClick}>
        <svg className="icon">
            <use xlinkHref={"#" + this.props.icon}></use>
        </svg>
      </span>
    );
  }
}
