import React from 'react';

import { ResourceFilterOption } from './resource_filter_option';

const api = '/api/v1/resources/?format=json'
const filterOptions = {
  'created_at': 'date',
  'title': 'alphabetical',
  'likes_count': 'liked',
  'tried_count': 'tried'
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
        <span>{this.props.resourceCount} Resources</span>
        <div className="resource-filter__controls">
          <p>Sort by</p>
          {Object.keys(filterOptions).map((filter, index) =>
            <ResourceFilterOption
              key={index}
              filter={filter}
              icon={filterOptions[filter]}
              active={this.props.ordering}
              handleClick={this.handleClick}/>
          )}
        </div>
      </div>
    );
  }
}
