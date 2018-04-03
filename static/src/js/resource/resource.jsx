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
    if (this.props.resource.is_private) {
        resourceClass = resourceClass + ' private' ;
    }

    return (
      <div className={resourceClass}>
        {resourceHeader}
        <div className="resource-summary">
            <a href={this.props.resource.url}>{this.props.resource.title}</a>
        </div>
        <footer className="resource-footer">
          <div className="resource-user">
            <div
                className="resource-user__group"
                style={{background: 'url(' + this.props.resource.organisation_logo + ') left center/contain no-repeat'}}>
            </div>
            <p className="resource-user__name">
              <a href={this.props.resource.created_by_link}>
                {this.props.resource.created_by}
              </a>
            </p>
          </div>
          <ResourceAction
            likes={this.props.resource.likes_count}
            tries={this.props.resource.tried_count}
          />
        </footer>
      </div>
    );
  }
}
