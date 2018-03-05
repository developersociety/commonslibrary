import React from 'react';
import ReactDOM from 'react-dom';

import { Resource } from './resource';


const ResourceData = require('./resources.json');

class ResourceList extends React.Component {
  constructor () {
    super()
    this.state = {
      resources: ResourceData
    }
  }

  render() {
    const resourcesList = this.state.resources.map((resource, index) =>
      <Resource
        key={resource.resource.id}
        resource={resource.resource}
      />
    )

    return(
      <div className="resources-grid">
        {resourcesList}
      </div>
    )
  }
}

ReactDOM.render(
  <ResourceList />,
  document.getElementById('react-app')
)
