import React from 'react';

import { SearchTags } from './search_tags';

const searchData = require('../data_sample/search.json');


export class Search extends React.Component {
  constructor () {
    super()
    this.state = {
      searchOptions: searchData
    }

    // handler binds
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    let query = event.target.value;

    if (query.length > 2) {
      // handle search query
    }
  }

  render() {
    return(
      <div className="search-bar">
        <form action="." className="search-form">
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
            <SearchTags searchOptions={this.state.searchOptions.tags}/>
            {/*<SearchGroups searchOptions={this.state.searchOptions}/>
            <SearchPeople searchOptions={this.state.searchOptions}/>*/}
          </div>
        </div>
      </div>
    )
  }
}
