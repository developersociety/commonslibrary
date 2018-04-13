import React from 'react';
import ReactDOM from 'react-dom';

import { Search } from './search/search';

import { Resource } from './resource/resource';
import { ResourceFilter } from './resource/resource_filter';

const pageUrl = new URL(window.location.href);

const api = '/api/v1/resources/?format=json'
const fixedOrganisation = document.getElementById('react-app').dataset.organisation;
const fixedUser = document.getElementById('react-app').dataset.user;
const preselectedTag = pageUrl.searchParams.get('tags');
const componentHolder = document.getElementById('react-app');
const csrf = componentHolder.querySelector('[name="csrfmiddlewaretoken"]').value

class ResourceList extends React.Component {
  constructor () {
    super()
    this.state = {
      resources: [],
      ordering: '&ordering=created_at',
      activeFilter: 'created_at',
      query: ''
    }

    // handler binds
    this.updateResourceOrder = this.updateResourceOrder.bind(this);
    this.updateResourceQuery = this.updateResourceQuery.bind(this);
    this.updateResourceList = this.updateResourceList.bind(this);
  }

  componentDidMount() {
    // if fixed Org or user then use that in initial query
    if (fixedOrganisation !== undefined) {
      this.setState(
        {
          query: '&organisation=' + fixedOrganisation
        },
        this.updateResourceList
      )
    } else if (fixedUser !== undefined) {
      this.setState(
        {
          query: '&created_by=' + fixedUser
        },
        this.updateResourceList
      )
    } else if (preselectedTag !== null) {
      this.setState(
        {
          query: '&tags=' + preselectedTag
        },
        this.updateResourceList
      )
    } else {
      this.updateResourceList()
    }
  }

  // Update resourse list order query from filter
  updateResourceOrder(filter) {
    let orderQuery = '&ordering=' + filter;

    if (filter == 'most_likes' || filter == 'most_tried') {
        orderQuery = '&' + filter + '=-resource'
    }
    this.setState({
        ordering: orderQuery,
        activeFilter: filter
      },
      this.updateResourceList
    )
  }

  // Update resourse list using query from form
  updateResourceQuery(newQuery) {
    this.setState({
        query: newQuery
      },
      this.updateResourceList
    )
    document.querySelector('#search_input').focus();
    // Scroll to a certain element
    document.getElementById('react-app').scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
    // Focus input field on new search
  }

  // Call API with resource list criteria
  updateResourceList() {
    let searchQuery = api + this.state.ordering + this.state.query;

    fetch(searchQuery, {
        method: 'get',
        credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => {
        this.setState({
          resources: data
        })
      })
  }

  render() {
    let resourceGridClass = 'resources-grid ';

    if (this.state.resources.length == 0) {
      resourceGridClass += 'no-resources';
    }

    return(
      <div className="resources">
        <Search
          updateResourceQuery={this.updateResourceQuery}
          fixedOrganisation={fixedOrganisation}
          fixedUser={fixedUser}
          preselectedTag={preselectedTag}
          />
        <ResourceFilter
          resourceCount={this.state.resources.length}
          activeFilter={this.state.activeFilter}
          updateResourceOrder={this.updateResourceOrder}
          />
        <div className={resourceGridClass}>
          {this.state.resources.map((resource, index) =>
            <Resource
              key={resource.id}
              resource={resource}
              csrf={csrf}
            />
          )}
        </div>
      </div>
    )
  }
}

ReactDOM.render(
  <ResourceList />,
  document.getElementById('react-app')
)
