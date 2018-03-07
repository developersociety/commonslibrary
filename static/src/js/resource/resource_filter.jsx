import React from 'react';

import { ResourceFilterOption } from './resource_filter_option';

export class ResourceFilter extends React.Component {
  constructor() {
    super();
    this.state = {
      activeFilter: 'date',
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

    // fake API call, replace with real one
    fetch('http://127.0.0.1:8080/static/src/js/data_sample/' + filter + '.json')
      .then(response => response.json())
      .then(newData => this.props.updateResourceList(newData));
  }

  render() {
    const active = this.state.activeFilter;
    const sortOptions = ['date', 'alphabetical', 'liked', 'tried']

    return (
      <div className="resources-filter">
        <span>{this.props.resourceCount} Resources</span>
        <div className="resource-filter__controls">
          <p>Sort by</p>
          {sortOptions.map((option, index) =>
            <ResourceFilterOption
              key={index}
              filter={option}
              className={'resource-filter__option ' + (active == option ? 'active' : '')}
              handleClick={this.handleClick}/>
          )}
        </div>
      </div>
    );
  }
}
