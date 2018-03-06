import React from 'react';

export class SearchTags extends React.Component {
  constructor() {
    super();

    this.state = {
      selectedTags: []
    }

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    let tag = e.target.textContent;

    // check if tag already in selectedTags
    if(!this.state.selectedTags.includes(tag)) {
      this.setState({
        selectedTags: [...this.state.selectedTags, e.target.textContent]
      })
    } else {
      let index = this.state.selectedTags.indexOf(tag);
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
    availableOptions.map((tag, index) =>
      !(selectedTags.includes(tag.option.name)) ? options.push(tag) : false
    )

    return (
      <div className="tag-list">
        {this.state.selectedTags.map((tag, index) =>
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
