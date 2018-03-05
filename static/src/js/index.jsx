import React from 'react';
import ReactDOM from 'react-dom';

import { Resource } from './resource';
import { ResourceFilter } from './resource_filter';


const ResourceData = require('./resources.json');

class ResourceList extends React.Component {
  constructor () {
    super()
    this.state = {
      resources: ResourceData
    }
    this.updateResourceList = this.updateResourceList.bind(this);
  }

  updateResourceList(newResourceList) {
    this.setState({
      resources: newResourceList
    })
  }

  render() {
    const resources = this.state.resources;
    const resourcesList = resources.map((resource, index) =>
      <Resource
        key={resource.resource.id}
        resource={resource.resource}
      />
    )

    return(
      <div className="resources">
        <ResourceFilter resourceCount={resources.length}/>
        <div className="resources-grid">
          {resourcesList}
        </div>
      </div>
    )
  }
}

ReactDOM.render(
  <ResourceList />,
  document.getElementById('react-app')
)
