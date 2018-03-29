import React from 'react';
import ReactDOM from 'react-dom';

import { Search } from './search/search';

import { Resource } from './resource/resource';
import { ResourceFilter } from './resource/resource_filter';

let api = '/api/v1/resources/?format=json'

class ResourceList extends React.Component {
  constructor () {
    super()
    this.state = {
      resources: [],
      ordering: 'created_at',
      query: ''
    }

    // handler binds
    this.updateResourceOrder = this.updateResourceOrder.bind(this);
    this.updateResourceQuery = this.updateResourceQuery.bind(this);
    this.updateResourceList = this.updateResourceList.bind(this);
  }

  componentDidMount() {
    this.updateResourceList()
  }

  // Update resourse list order query from filter
  updateResourceOrder(filter) {
    this.setState(
      {
        ordering: filter
      },
      this.updateResourceList
    )
  }

  // Update resourse list using query from form
  updateResourceQuery(newQuery) {
    this.setState(
      {
        query: newQuery
      },
      this.updateResourceList
    )
  }

  // Call API with resource list criteria
  updateResourceList() {
    let searchQuery = api + '&ordering=' + this.state.ordering + this.state.query;

    fetch(searchQuery, {
        method: 'get',
        credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => {
        this.setState({
          resources: data
        })
      })
  }

  render() {
    return(
      <div className="resources">
        <Search
          updateResourceQuery={this.updateResourceQuery}
          />
        <ResourceFilter
          resourceCount={this.state.resources.length}
          ordering={this.state.ordering}
          updateResourceOrder={this.updateResourceOrder}
          />
        <div className="resources-grid">
          {this.state.resources.map((resource, index) =>
            <Resource
              key={resource.id}
              resource={resource}
            />
          )}
        </div>
      </div>
    )
  }
}

ReactDOM.render(
  <ResourceList />,
  document.getElementById('react-app')
)
