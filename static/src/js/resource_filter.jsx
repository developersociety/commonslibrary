import React from 'react';

export class ResourceFilter extends React.Component {
  constructor() {
    super();
    this.state = {
      activeFilter: 'date',
      order: 'forward'
    }
  }

  handleClick(filter, e) {
    this.setState(prevState => ({
      activeFilter: filter,
      order: prevState.activeFilter == filter ? 'reverse' : prevState.order
    }));
  }

  render() {
    return (
      <div className="resources-filter">
        <span>{this.props.resourceCount} Resources</span>
        <div className="resource-filter__controls">
          <p>Sort by</p>
          <span
            className="resource-filter__option"
            onClick={(e) => this.handleClick('date', e)}>
            <svg className="icon">
              <use xlinkHref="#calendar"></use>
            </svg>
          </span>
          <span
            className="resource-filter__option"
            onClick={(e) => this.handleClick('alphabetical', e)}>
            A-Z
          </span>
          <span
            className="resource-filter__option"
            onClick={(e) => this.handleClick('liked', e)}>
            <svg className="icon">
              <use xlinkHref="#liked"></use>
            </svg>
          </span>
          <span
            className="resource-filter__option"
            onClick={(e) => this.handleClick('tried', e)}>
            <svg className="icon">
              <use xlinkHref="#tried"></use>
            </svg>
          </span>
        </div>
      </div>
    );
  }
}
