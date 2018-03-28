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
    this.state = {
      activeFilter: 'created_at',
      reserve: false
    }

    // handler binds
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(filter, e) {
    this.setState(prevState => ({
      activeFilter: filter,
      reverse: !prevState.reverse
    }));

    this.props.updateResourceOrder(filter, this.state.reverse)
  }

  render() {
    const active = this.state.activeFilter;

    return (
      <div className="resources-filter">
        <span>{this.props.resourceCount} Resources</span>
        <div className="resource-filter__controls">
          <p>Sort by</p>
          {Object.keys(filterOptions).map((index, option) =>
            <ResourceFilterOption
              key={option}
              filter={index}
              icon={filterOptions[index]}
              className={'resource-filter__option ' + (active == index ? 'active' : '')}
              handleClick={this.handleClick}/>
          )}
        </div>
      </div>
    );
  }
}
