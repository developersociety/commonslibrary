import React from 'react';

import { ResourceFilterOption } from './resource_filter_option';

const alphabeticalData = require('../data_sample/alphabetical.json');
const dateData = require('../data_sample/date.json');
const likedData = require('../data_sample/liked.json');
const triedData = require('../data_sample/tried.json');

const dataOrders = {
    'date': dateData,
    'alphabetical': alphabeticalData,
    'liked': likedData,
    'tried': triedData
}

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
    let newData = dataOrders[filter];

    this.props.updateResourceList(newData);
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
