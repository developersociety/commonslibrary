import React from 'react';

import { SearchOptionManager } from './search_option_manager';

export class Search extends React.Component {
  constructor () {
    super()
    this.state = {
      searchTagsOptions: [],
      searchOrganisationsOptions: [],
      searchPeopleOptions: [],
      searchQuery: '',
      searchOptionsSelected: 0
    }

    // handler binds
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleSelection = this.handleSelection.bind(this);
    this.fetchTagsData = this.fetchTagsData.bind(this);
    this.fetchOrganisationsData = this.fetchOrganisationsData.bind(this);
    this.fetchPeopleData = this.fetchPeopleData.bind(this);
  }

  fetchTagsData(query) {
    fetch('/api/v1/tags' + '?search=' + query, {
        method: 'get',
        credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => {
        this.setState({
          searchTagsOptions: data
        })
      })
  }

  fetchOrganisationsData(query) {
    fetch('/api/v1/organisations' + '?search=' + query, {
        method: 'get',
        credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => {
        this.setState({
          searchOrganisationsOptions: data
        })
      })
  }

  fetchPeopleData(query) {
    fetch('/api/v1/users' + '?search=' + query, {
        method: 'get',
        credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => {
        this.setState({
          searchPeopleOptions: data
        })
      })
  }

  handleSelection(optionStep) {
    // track number of selected search options
    this.setState(prevState => ({
      searchOptionsSelected: prevState.searchOptionsSelected + optionStep
    })
  )}

  handleChange(event) {
    let query = event.target.value;

    this.setState({
      searchQuery: query
    });

    // If query longer that 2, fetch data and set state
    if (query.length > 2) {
      this.fetchTagsData(query)
      this.fetchOrganisationsData(query)
      this.fetchPeopleData(query)
    } else {
      this.setState({
        searchTagsOptions: [],
        searchOrganisationsOptions: [],
        searchPeopleOptions: [],
      })
    }

  }

  handleSubmit(event) {
    event.preventDefault();
    let tags = this.searchTags.state.selectedOptions;
    let groups = this.searchOrganisations.state.selectedOptions;
    let people = this.searchPeople.state.selectedOptions;
    let query = this.state.searchQuery
  }

  render() {
    // Only show search if options are available or selected in previous search
    const showSearch = this.searchOptionsSelected > 0
        || this.state.searchTagsOptions.length > 0
        || this.state.searchOrganisationsOptions.length > 0
        || this.state.searchPeopleOptions.length > 0;

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

        {showSearch == true &&
          <div className="search-filter">

            <div className="search-filter__tags">
              <div className="search-filter__type">
                <span>Tags</span>
                <svg className="icon">
                  <use xlinkHref="#tag"></use>
                </svg>
              </div>
              <SearchOptionManager
                ref={(searchTags) => {this.searchTags = searchTags;}}
                searchOptions={this.state.searchTagsOptions}
                handleSelection={this.handleSelection}/>
            </div>

            <div className="search-filter__groups">
              <div className="search-filter__type">
                <span>Groups</span>
                <svg className="icon">
                  <use xlinkHref="#groups"></use>
                </svg>
              </div>
              <SearchOptionManager
                ref={(searchOrganisations) => {this.searchOrganisations = searchOrganisations;}}
                searchOptions={this.state.searchOrganisationsOptions}
                handleSelection={this.handleSelection}/>
            </div>

            <div className="search-filter__people">
              <div className="search-filter__type">
                <span>People</span>
                <svg className="icon">
                  <use xlinkHref="#directory"></use>
                </svg>
              </div>
              <SearchOptionManager
                ref={(searchPeople) => {this.searchPeople = searchPeople;}}
                searchOptions={this.state.searchPeopleOptions}
                handleSelection={this.handleSelection}/>
            </div>
          </div>
        }
      </div>
    )
  }
}
