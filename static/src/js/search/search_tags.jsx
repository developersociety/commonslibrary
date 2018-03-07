import React from 'react';

export class SearchTags extends React.Component {
  constructor() {
    super();
    this.state = {
      selectedTags: []
    }

    // handler binds
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    let tag = e.target.textContent;
    let index = this.state.selectedTags.indexOf(tag);

    // Check if tag already in selectedTags
    if(index === -1) {
      this.setState({
        selectedTags: [...this.state.selectedTags, e.target.textContent]
      })
    }
    else {
      let newSelected = this.state.selectedTags;

      // remove item
      newSelected.splice(index, 1);
      this.setState({
        selectedTags: newSelected
      })
    }
  }

  render() {
    let options = [];
    let availableOptions = this.props.searchOptions;
    let selectedTags = this.state.selectedTags;

    // look through available options and remove elements already selected
    availableOptions.map(tag => {
      if (!selectedTags.includes(tag.option.name)) {
        return options.push(tag);
      }
    })

    return (
      <div className="tag-list">
        {selectedTags.map((tag, index) =>
          <div
            key={index}
            className="tag active"
            onClick={this.handleClick}>
            {tag}
          </div>
        )}
        {options.map((tag, index) =>
          <div
            key={index}
            className="tag"
            onClick={this.handleClick}
            id={tag.option.slug}>
            {tag.option.name}
          </div>
        )}
      </div>
    )
  }
}
