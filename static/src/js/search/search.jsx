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

  // Get tags data from API based on query
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

  // Get organisations data from API based on query
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

  // Get people data from API based on query
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

  // Track number of selected search options
  handleSelection(increment) {
    this.setState(prevState => ({
      searchOptionsSelected: prevState.searchOptionsSelected + increment
    })
  )}

  // Watch input field for changes
  handleChange(event) {
    let query = event.target.value;

    this.setState({
      searchQuery: query
    });

    // If query longer that 2, fetch data from API and set state
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

    // Get current selected tags from child state
    const query = this.state.searchQuery;
    const tags = this.searchTags.state.selectedOptions;
    const organisations = this.searchOrganisations.state.selectedOptions;
    const people = this.searchPeople.state.selectedOptions;

    // map through selected options add prefix if more than one value
    let tagQuery = tags.map(tag => tag.id).join('&tags=');
    let organisationQuery = organisations.map(organisations => organisations.id).join('&organisation=');
    let peopleQuery = people.map(people => people.id).join('&created_by=');

    // If fixed organisation was set in template use that
    if (this.props.fixedOrganisation !== undefined) {
        organisationQuery = this.props.fixedOrganisation;
    }
    if (this.props.fixedUser !== undefined) {
        peopleQuery = this.props.fixedUser;
    }

    // Add search queries to object
    const searchCriteria = {
      tags: tagQuery,
      organisation: organisationQuery,
      created_by: peopleQuery
    }

    let searchQuery = '';

    // If no tags selected use search query, else loop through selected options and create query
    if (query != '' && tags.length == 0 && organisations.length == 0 && people.length == 0) {
      searchQuery = '&search=' + query;
    } else {
      {Object.keys(searchCriteria).map((query, index) => {
        if (searchCriteria[query] != '') {
          searchQuery += ('&' + query + '=' + searchCriteria[query])
        }
      })}
    }

    // Create search query string from selected options
    this.props.updateResourceQuery(searchQuery);
  }

  render() {
    // Only show search if options are available or selected in previous search
    const showSearch = this.state.searchOptionsSelected > 0
        || this.state.searchTagsOptions.length > 0
        || this.state.searchOrganisationsOptions.length > 0
        || this.state.searchPeopleOptions.length > 0;

    const showOrganisation = this.props.fixedOrganisation == undefined;
    const showPeople = this.props.fixedUser == undefined;

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

        <div className={"search-filter show-" + showSearch}>
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

          <div className={'search-filter__groups shown-' + showOrganisation}>
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

          <div className={'search-filter__people shown-' + showPeople}>
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

        {this.state.searchQuery.length > 0 &&
          <div className="search-prompt">
            <p>Click blocks to add them to your search, or just hit return for a keyword search.</p>
          </div>
        }
      </div>
    )
  }
}
