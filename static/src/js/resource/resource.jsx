import React from 'react';

export class Resource extends React.Component {
    animationDelay(index) {}

    render() {
        let resourceClass = 'resource';
        let resourceHeader = null;
        let resourceOrgLogo = null;

        const animationStyles = {
            animationDelay: `${(this.props.index % 20) * 0.05}s`
        };

        if (this.props.resource.image) {
            resourceClass += ' with-image';
            resourceHeader = (
                <header
                    className="resource-image"
                    style={{ backgroundImage: `url(${this.props.resource.image})` }}
                />
            );
        }
        if (this.props.resource.is_private) {
            resourceClass += ' private';
        }
        if (this.props.resource.organisation_logo) {
            resourceOrgLogo = (
                <div
                    className="resource-user__group"
                    style={{
                        background: `url(${
                            this.props.resource.organisation_logo
                        }) left center/contain no-repeat`
                    }}
                />
            );
        }

        return (
            <a href={this.props.resource.url} className={resourceClass} style={animationStyles}>
                {resourceHeader}
                <div className="resource-summary">{this.props.resource.title}</div>
                <footer className="resource-footer">
                    <div className="resource-user">
                        {resourceOrgLogo}
                        <p className="resource-user__name">{this.props.resource.created_by}</p>
                    </div>
                    <div className="resource-actions">
                        <span className={`resource-liked ${this.props.resource.user_liked}`}>
                            <svg className="icon">
                                <use xlinkHref="#liked" />
                            </svg>
                            {this.props.resource.likes_count}
                        </span>
                        <span className={`resource-tried ${this.props.resource.user_tried}`}>
                            <svg className="icon">
                                <use xlinkHref="#tried" />
                            </svg>
                            {this.props.resource.tried_count}
                        </span>
                    </div>
                </footer>
            </a>
        );
    }
}
