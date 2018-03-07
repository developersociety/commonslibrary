import React from 'react';

import { SearchOption } from './search_option';


export class SearchOptionManager extends React.Component {
  constructor() {
    super();
    this.state = {
      selectedOptions: []
    }

    // handler binds
    this.handleOptionSelection = this.handleOptionSelection.bind(this);
  }

  handleOptionSelection(tag) {
    let prevSelected = this.state.selectedOptions;
    let index = prevSelected.indexOf(tag);

    // if not in state add else remove
    if(index === -1) {
      this.setState(newState => {
        newState.selectedOptions.push(tag)
        return { selectedOptions: newState.selectedOptions }
      })
    } else {
      this.setState(newState => {
        newState.selectedOptions.splice(index, 1)
        return { selectedOptions: newState.selectedOptions }
      })
    }
  }

  render() {

    return (
      <div className="tag-list">
        {this.state.selectedOptions.map((tag, index) =>
          <SearchOption
            key={tag.id}
            option={tag}
            name = {tag.name}
            active={true}
            handleOptionSelection={this.handleOptionSelection} />

        )}
        {this.props.searchOptions.map((tag, index) => {
          if (!this.state.selectedOptions.includes(tag.option)) {
            return (
              <SearchOption
                key={tag.option.id}
                option={tag.option}
                handleOptionSelection={this.handleOptionSelection} />
            )
          }
        })}
      </div>
    )
  }
}
