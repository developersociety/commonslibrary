import React from 'react';
import ReactDOM from 'react-dom';

import { Search } from './search/search.jsx';
import { Resource } from './resource/resource.jsx';
import { ResourceFilter } from './resource/resource_filter.jsx';

const allResourcesApi = '/api/v1/resources/?format=json';
const featuredResourcesApi = '/api/v1/resources/favourites/?format=json';
const hideSearch = document.getElementById('react-app').dataset.hidesearch == 'true' || false;
const fixedOrganisation = document.getElementById('react-app').dataset.organisation;
const fixedCategory = document.getElementById('react-app').dataset.category;
const fixedUser = document.getElementById('react-app').dataset.user;
const preselectedTag = location.search.split('tags=')[1];
const componentHolder = document.getElementById('react-app');
const csrf = componentHolder.querySelector('[name="csrfmiddlewaretoken"]').value;

class ResourceList extends React.Component {
    constructor() {
        super();
        this.state = {
            hasSearched: false,
            resources: [],
            resourcesCount: 0,
            resourcesNextPage: null,
            ordering: '&ordering=-created_at',
            activeFilter: '-created_at',
            hideSearch: hideSearch,
            query: ''
        };

        // handler binds
        this.updateResourceOrder = this.updateResourceOrder.bind(this);
        this.updateResourceQuery = this.updateResourceQuery.bind(this);
        this.updateResourceList = this.updateResourceList.bind(this);
        this.nextResourceList = this.nextResourceList.bind(this);
    }

    componentDidMount() {
        // if fixed Org, Tag, or User then use that in initial query
        if (fixedOrganisation !== undefined) {
            this.setState(
                {
                    query: `&organisation=${fixedOrganisation}`
                },
                this.updateResourceList
            );
        }
        if (fixedCategory !== undefined) {
            this.setState(
                {
                    query: `&categories=${fixedCategory}&page_size=100`
                },
                this.updateResourceList
            );
        } else if (fixedUser !== undefined) {
            this.setState(
                {
                    query: `&created_by=${fixedUser}`
                },
                this.updateResourceList
            );
        } else if (preselectedTag !== undefined) {
            this.setState(
                {
                    query: `&tags=${preselectedTag}`
                },
                this.updateResourceList
            );
        } else {
            this.updateResourceList();
        }
    }

    // Update resourse list order query from filter
    updateResourceOrder(filter) {
        let orderQuery = `&ordering=${filter}`;

        if (filter === 'most_likes' || filter === 'most_tried') {
            orderQuery = `&${filter}=-resource`;
        }
        this.setState(
            {
                ordering: orderQuery,
                activeFilter: filter
            },
            this.updateResourceList
        );
    }

    // Update resourse list using query from form
    updateResourceQuery(newQuery) {
        this.setState(
            {
                query: newQuery
            },
            this.updateResourceList
        );
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
        const searchQuery = allResourcesApi + this.state.ordering + this.state.query;

        fetch(searchQuery, {
            method: 'get',
            credentials: 'same-origin'
        })
            .then((response) => response.json())
            .then((data) => {
                this.setState({
                    hasSearched: true,
                    resources: data.results,
                    resourcesCount: data.count,
                    resourcesNextPage: data.next
                });
            });
    }

    //HERE!!!!!!
    // Call API for featured resources
    // getFeaturedResources() {

        //but I can't use state here without intefering with
        //how state is being used for the main resources
        const [featuredResourcesData, setFeaturedResourcesData] = useState([])

        const fetchFeaturedResources = () => {
            fetch(featuredResourcesApi)
            .then (response => {return response.json()})
            .then (featuredResourcesData => {setFeaturedResourcesData(featuredResourcesData)})
        }

        useEffect(() => {
            fetchFeaturedResources()
        }, [])

        // return (
        //     <div>

        //     </div>
        // )
    // }

    useEffect(() => {
        fetchFeaturedResources()
    }, [])

    nextResourceList(event) {
        event.persist();
        event.target.classList.add('loading');

        fetch(this.state.resourcesNextPage, {
            method: 'get',
            credentials: 'same-origin'
        })
            .then((response) => response.json())
            .then((data) => {
                const mergedResourceList = this.state.resources.concat(data.results);

                this.setState({
                    resources: mergedResourceList,
                    resourcesCount: data.count,
                    resourcesNextPage: data.next
                });

                event.target.classList.remove('loading');
            });
    }

    render() {
        let resourceGridClass = 'resources-grid ';
        let loadMoreResources = '';

        if (this.state.resources.length === 0 && this.state.hasSearched) {
            resourceGridClass += 'no-resources';
        } else if (!this.state.hasSearched) {
            resourceGridClass += 'loading-resources';
        }

        if (this.state.resourcesNextPage !== null) {
            loadMoreResources = (
                <div className="load-more">
                    <span className="button" onClick={this.nextResourceList}>
                        Load more
                        <div className="load-more__circle" />
                    </span>
                </div>
            );
        }

        return (
            <div className="resources">
                {this.state.hideSearch == false && (
                    <Search
                        updateResourceQuery={this.updateResourceQuery}
                        fixedOrganisation={fixedOrganisation}
                        fixedUser={fixedUser}
                        preselectedTag={preselectedTag}
                    />
                )}
                {/* <FeaturesResources /> */}
                <ResourceFilter
                    resourceCount={this.state.resourcesCount}
                    activeFilter={this.state.activeFilter}
                    updateResourceOrder={this.updateResourceOrder}
                />
                <div className={resourceGridClass}>
                    {this.state.resources.map((resource, index) => (
                        <Resource key={resource.id} resource={resource} csrf={csrf} index={index} />
                    ))}
                    {loadMoreResources}
                </div>
            </div>
        );
    }
}

ReactDOM.render(<ResourceList />, document.getElementById('react-app'));
