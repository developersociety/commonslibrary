import React from 'react';

import { SearchOption } from './search_option';


export class SearchOptionManager extends React.Component {
  constructor() {
    super();
    this.state = {
      selectedOptions: []
    }

    // handler binds
    this.checkSelected = this.checkSelected.bind(this);
    this.handleOptionSelection = this.handleOptionSelection.bind(this);
  }

  checkSelected(option) {
    let inSelected = false
    let inSelectedIndex = -1
    this.state.selectedOptions.map((selectedOption, index) => {
      if (JSON.stringify(selectedOption) === JSON.stringify(option)) {
        inSelected = true;
        inSelectedIndex = index;
      }
    })
    return {
      selected: inSelected,
      index: inSelectedIndex
    }
  }

  handleOptionSelection(option) {
    let prevSelected = this.state.selectedOptions;
    let checkSelected = this.checkSelected(option);

    // if not in state add, else remove
    if(!checkSelected.selected) {
      this.setState(newState => {
        newState.selectedOptions.push(option)
        return { selectedOptions: newState.selectedOptions }
      })
      this.props.handleSelection(1);
    } else {
      this.setState(newState => {
        newState.selectedOptions.splice(checkSelected.index, 1)
        return { selectedOptions: newState.selectedOptions }
      })
      this.props.handleSelection(-1);
    }
  }

  render() {
    let searchOptions = []
    this.props.searchOptions.map(tag => {
      if (!this.checkSelected(tag).selected) {
        searchOptions.push(tag)
      }
    })

    return (
      <div className="tag-list">
        {this.state.selectedOptions.map(tag =>
          <SearchOption
            key={tag.id}
            option={tag}
            name = {tag.name}
            active={true}
            handleOptionSelection={this.handleOptionSelection} />

        )}
        {searchOptions.map(tag =>
          <SearchOption
            key={tag.id}
            option={tag}
            handleOptionSelection={this.handleOptionSelection} />
        )}
        {(this.state.selectedOptions.length == 0 && searchOptions.length == 0) &&
          <div className="tag inactive">None selected</div>
        }
      </div>
    )
  }
}
