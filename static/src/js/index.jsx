import React from 'react';
import ReactDOM from 'react-dom';

import { Search } from './search/search';

import { Resource } from './resource/resource';
import { ResourceFilter } from './resource/resource_filter';


const resourceData = require('./data_sample/resources.json');

class ResourceList extends React.Component {
  constructor () {
    super()
    this.state = {
      resources: resourceData
    }

    // handler binds
    this.updateResourceList = this.updateResourceList.bind(this);
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
              key={resource.resource.id}
              resource={resource.resource}
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
