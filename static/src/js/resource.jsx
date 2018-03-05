import React from 'react';

import { ResourceAction } from './resource_action';

export class Resource extends React.Component {
  render() {
    const resource = this.props.resource;

    let resourceClass = 'resource';
    let resourceHeader = null;

    if (resource.image) {
      resourceClass = resourceClass + ' with-image';
      resourceHeader = (
        <header className='resource-image' style={{backgroundImage: 'url(' + resource.image + ')'}}>
        </header>
      );
    }

    return (
      <div className={resourceClass}>
        {resourceHeader}
        <div className="resource-summary">{resource.summary}</div>
        <footer className="resource-footer">
          <div className="resource-user">
            <div className="resource-user__org">{resource.group}</div>
            <p className="resource-user__name">{resource.user}</p>
          </div>
          <ResourceAction
            likes={resource.likes}
            tries={resource.tries}
          />
        </footer>
      </div>
    );
  }
}
