import React from 'react';

export class Resource extends React.Component {
  render() {
    let resourceClass = 'resource';
    let resourceHeader = null;
    let resourceOrgLogo = null;

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
    if (this.props.resource.organisation_logo) {
      resourceOrgLogo = (
        <div
          className="resource-user__group"
          style={{background: 'url(' + this.props.resource.organisation_logo + ') left center/contain no-repeat'}}>
        </div>
      )
    }

    return (
      <a href={this.props.resource.url} className={resourceClass}>
        <div className="resource-blurred">
          {resourceHeader}
          <div className="resource-summary">
            {this.props.resource.title}
          </div>
          <footer className="resource-footer">
            <div className="resource-user">
              {resourceOrgLogo}
              <p className="resource-user__name">
                {this.props.resource.created_by}
              </p>
            </div>
            <div className="resource-actions">
              <span
                className={'resource-liked ' + (this.props.resource.user_liked)}>
                <svg className="icon">
                  <use xlinkHref="#liked"></use>
                </svg>
                {this.props.resource.likes_count}
              </span>
              <span
                className={'resource-tried ' + (this.props.resource.user_tried)}>
                <svg className="icon">
                  <use xlinkHref="#tried"></use>
                </svg>
                {this.props.resource.tried_count}
              </span>
            </div>
          </footer>
        </div>
        <div className="resource-focused">
          <div className="resource-list-abstract">
            <p className="resource-abstract">
              {this.props.resource.abstract}
            </p>
          </div>
          <div className="resource-meta">
            <div className="icon-list">
              <div className="icon-list__row">
                <svg className="icon">
                  <use xlinkHref="#date"></use>
                </svg>
                <div className="icon-list__content">
                  <p>{this.props.resource.created_at}</p>
                </div>
              </div>

              {this.props.resource.tags &&
                <div className="icon-list__row">
                  <svg className="icon">
                    <use xlinkHref="#tag"></use>
                  </svg>
                  <div className="icon-list__content">
                    {this.props.resource.tags.map((tag, index) => {
                      return index != (this.props.resource.tags.length - 1) ? tag.title + ', ' : tag.title
                    })}
                  </div>
                </div>
              }
            </div>
          </div>
        </div>
      </a>
    );
  }
}
