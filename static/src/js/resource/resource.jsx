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
                <div className="resource-blurred">
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
                </div>
                <div className="resource-focused">
                    <div className="resource-list-abstract">
                        <p className="resource-abstract">{this.props.resource.abstract}</p>
                    </div>
                    <div className="resource-meta">
                        <div className="icon-list">
                            <div className="icon-list__row">
                                <svg className="icon">
                                    <use xlinkHref="#date" />
                                </svg>
                                <div className="icon-list__content">
                                    <p>{this.props.resource.created_at}</p>
                                </div>
                            </div>

                            {this.props.resource.tags.length > 0 && (
                                <div className="icon-list__row">
                                    <svg className="icon">
                                        <use xlinkHref="#tag" />
                                    </svg>
                                    <div className="icon-list__content">
                                        {this.props.resource.tags.map((tag, index) =>
                                            index != this.props.resource.tags.length - 1
                                                ? tag.title + ', '
                                                : tag.title
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </a>
        );
    }
}
