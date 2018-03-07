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

  handleOptionSelection(option) {
    let prevSelected = this.state.selectedOptions;
    let index = prevSelected.indexOf(option);

    // if not in state add, else remove
    if(index === -1) {
      this.setState(newState => {
        newState.selectedOptions.push(option)
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
    console.log('starting render ' + this.props.type)
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
        {this.props.searchOptions.map(tag => {
          if (!this.state.selectedOptions.includes(tag.option)) {
            console.log(tag.option, this.state.selectedOptions)
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
