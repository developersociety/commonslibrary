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
    this.updateResourceList = this.updateResourceList.bind(this);
  }

  componentDidMount() {
    fetch(api)
      .then(response => response.json())
      .then(data => this.setState({
        resources: data
      }))
  }

  updateResourceList(newResourceList) {
    this.setState({
      resources: newResourceList
    })
  }

  render() {
    return(
      <div className="resources">
        <Search />
        <ResourceFilter
          resourceCount={this.state.resources.length}
          updateResourceList={this.updateResourceList}/>
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
