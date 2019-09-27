import React from 'react';

import { ResourceFilterOption } from './resource_filter_option.jsx';

const api = '/api/v1/resources/?format=json'
const filterOptions = {
  'created_at': 'date',
  'title': 'alphabetical',
  'most_likes': 'liked',
  'most_tried': 'tried'
}

export class ResourceFilter extends React.Component {
  constructor() {
    super();

    // handler binds
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(filter, e) {
    this.props.updateResourceOrder(filter)
  }

  render() {
    return (
      <div className="resources-filter">
        <span>{this.props.resourceCount} Resource{this.props.resourceCount != 1 ? 's' : ''}</span>
        <div className="resource-filter__controls">
          <p>Sort by</p>
          {Object.keys(filterOptions).map((filter, index) =>
            <ResourceFilterOption
              key={index}
              filter={filter}
              icon={filterOptions[filter]}
              active={this.props.activeFilter}
              handleClick={this.handleClick}/>
          )}
        </div>
      </div>
    );
  }
}
