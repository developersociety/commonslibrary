import React from 'react';

import { ResourceAction } from './resource_action';

export class Resource extends React.Component {
  render() {
    let resourceClass = 'resource';
    let resourceHeader = null;

    if (this.props.resource.image) {
      resourceClass = resourceClass + ' with-image';
      resourceHeader = (
        <header className='resource-image' style={{backgroundImage: 'url(' + this.props.resource.image + ')'}}>
        </header>
      );
    }

    return (
      <div className={resourceClass}>
        {resourceHeader}
        <div className="resource-summary">{this.props.resource.summary}</div>
        <footer className="resource-footer">
          <div className="resource-user">
            <div
                className="resource-user__group"
                style={{background: 'url(' + this.props.resource.group + ') left center/contain no-repeat'}}>
            </div>
            <p className="resource-user__name">{this.props.resource.user}</p>
          </div>
          <ResourceAction
            likes={this.props.resource.likes}
            tries={this.props.resource.tries}
          />
        </footer>
      </div>
    );
  }
}
