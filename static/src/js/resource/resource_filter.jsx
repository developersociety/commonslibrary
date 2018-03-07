import React from 'react';

export class ResourceFilter extends React.Component {
  constructor() {
    super();
    this.state = {
      activeFilter: 'date',
      reserve: false
    }
  }

  handleClick(filter, e) {
    this.setState(prevState => ({
      activeFilter: filter,
      order: prevState.activeFilter == filter ? !prevState.reverse : false
    }));

    // fake API call
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
            <span
              key={index}
              className={'resource-filter__option ' + (active == option ? 'active' : '')}
              onClick={(e) => this.handleClick(option, e)}
              data='test data'
              id={option}>
              {option}
            </span>
          )}
        </div>
      </div>
    );
  }
}
