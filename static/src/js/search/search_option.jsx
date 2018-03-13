import React from 'react';

export class SearchOption extends React.Component {
  constructor() {
    super();

    this.optionClick = this.optionClick.bind(this);
  }

  optionClick() {
    this.props.handleOptionSelection(this.props.option)
  }

  render() {
    let activeClass = this.props.active ? 'tag active' : 'tag';
    let optionIcon = (<svg className="icon"><use xlinkHref="#add"></use></svg>);

    if (this.props.active) {
      optionIcon = (<svg className="icon"><use xlinkHref="#remove"></use></svg>);
    }

    return (
      <div
        className={activeClass}
        onClick={this.optionClick}>
        {this.props.option.name}
        {optionIcon}
      </div>
    )
  }
}
