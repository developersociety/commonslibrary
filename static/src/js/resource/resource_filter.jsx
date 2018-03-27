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
      order: prevState.activeFilter == filter ? !prevState.reverse : false
    }));

    this.props.updateResourceOrder(filter)
  }

  render() {
    const active = this.state.activeFilter;
    const sortOptions = ['created_at', 'title', 'likes_count', 'tried_count']

    return (
      <div className="resources-filter">
        <span>{this.props.resourceCount} Resources</span>
        <div className="resource-filter__controls">
          <p>Sort by</p>
          {sortOptions.map((option, index) =>
            <ResourceFilterOption
              key={index}
              filter={option}
              icon={filterOptions[option]}
              className={'resource-filter__option ' + (active == option ? 'active' : '')}
              handleClick={this.handleClick}/>
          )}
        </div>
      </div>
    );
  }
}
