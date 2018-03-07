import React from 'react';

import { SearchOptionManager } from './search_option_manager';

const searchData = require('../data_sample/search.json');


export class Search extends React.Component {
  constructor () {
    super()
    this.state = {
      searchOptions: searchData
    }

    // handler binds
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    let query = event.target.value;

    if (query.length > 2) {
      // handle search query
    }
  }

  handleSubmit(event) {
    event.preventDefault();
    let tags = this.searchTags.state.selectedOptions;
    let groups = this.searchGroups.state.selectedOptions;
    let people = this.searchPeople.state.selectedOptions;
  }

  render() {
    return(
      <div className="search-bar">
        <form onSubmit={this.handleSubmit} className="search-form">
          <input
            type="text"
            placeholder="Type here to search for resource"
            onChange={this.handleChange}/>
          <button type="submit">
            <svg className="icon">
              <use xlinkHref="#search"></use>
            </svg>
          </button>
        </form>

        <div className="search-filter">
          <div className="search-filter__tags">
            <p className="search-filter__type">Tags</p>
            <SearchOptionManager
              ref={(searchTags) => {this.searchTags = searchTags;}}
              searchOptions={this.state.searchOptions.tags}/>
          </div>
          <div className="search-filter__groups">
            <p className="search-filter__type">Groups</p>
            <SearchOptionManager
              ref={(searchGroups) => {this.searchGroups = searchGroups;}}
              searchOptions={this.state.searchOptions.groups}/>
          </div>
          <div className="search-filter__people">
            <p className="search-filter__type">People</p>
            <SearchOptionManager
              ref={(searchPeople) => {this.searchPeople = searchPeople;}}
              searchOptions={this.state.searchOptions.people}/>
          </div>
        </div>
      </div>
    )
  }
}
