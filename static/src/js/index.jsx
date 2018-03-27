import React from 'react';
import ReactDOM from 'react-dom';

import { Search } from './search/search';

import { Resource } from './resource/resource';
import { ResourceFilter } from './resource/resource_filter';

const api = '/api/v1/resources/?format=json'

class ResourceList extends React.Component {
  constructor () {
    super()
    this.state = {
      resources: []
    }

    // handler binds
    this.updateResourceOrder = this.updateResourceOrder.bind(this);
  }

  componentDidMount() {
    fetch(api, {
        method: 'get',
        credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => this.setState({
        resources: data
      }))
  }

  updateResourceOrder(filter) {
    fetch(api + '&ordering=' + filter, {
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
        <Search />
        <ResourceFilter
          resourceCount={this.state.resources.length}
          updateResourceOrder={this.updateResourceOrder}/>
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
