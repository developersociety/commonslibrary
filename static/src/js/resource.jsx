import React from 'react';

export class Resource extends React.Component {
  render() {
    return (
      <div className="resource with-image">
        <header className="resource-image">
        </header>
        <div className="resource-summary">{this.props.summary}</div>
        <footer className="resource-footer">
          <div className="resource-user">
            <div className="resource-user__org">{this.props.group}</div>
            <p className="resource-user__name">{this.props.user}</p>
          </div>
        </footer>
      </div>
    );
  }
}
