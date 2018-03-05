import React from 'react';

import { ResourceAction } from './resource_action';

export class Resource extends React.Component {
  render() {
    const resource = this.props.resource;

    return (
      <div className="resource with-image">
        <header className="resource-image">
        </header>
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
